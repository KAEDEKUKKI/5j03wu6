from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user

from system.camera import CameraStreamer
from permissions.models import UserGroup

from . import main_bp
from .form import ManualConfigForm, DeviceForm
from .models import Device, DeviceType

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ManualConfigForm(request.form)
    form.device_type.choices = [(type.id, type.name) for type in DeviceType.get_all()]

    if form.validate_on_submit():
        d_name = form.device_name.data
        d_type = form.device_type.data
        ip = form.ip_address.data
        port = form.protocol_port.data

        new_device = Device(d_name, d_type, ip, port)

        existing_device = Device.get_by_ip(new_device.ip_address, new_device.protocol_port)
        if existing_device:
            flash('A device with the same IP already exists.', 'alert-warning')
            return redirect(url_for('main.index'))

        # Create the new device
        device_id = new_device.create()

        if device_id:
            flash('Device paired successfully!', 'alert-success')
            return redirect(url_for('main.index'))
        else:
            flash('Failed to pair the device. Please try again.', 'alert-danger')

    if UserGroup.is_admin(current_user.id):
        devices = Device.get_all_devices()
    else:
        devices = []

    return render_template('main/index.html', form=form, devices=devices)

@main_bp.route('/device/<int:device_id>', methods=['GET', 'POST'])
@login_required
def device_view(device_id):
    form = DeviceForm(request.form)
    device = Device.get_by_id(device_id)

    if form.validate_on_submit():
        deleted_id = device.delete()

        if deleted_id:
            flash(f'Device with ID {deleted_id} deleted successfully!', 'alert-success')
            return redirect(url_for('main.index'))
        else:
            flash('Failed to delete the device. Please try again.', 'alert-danger')

    return render_template('main/device_view.html', form=form, device=device)

@main_bp.route('/video_feed/<string:ip>:<int:port>', methods=['GET', 'POST'])
@login_required
def video_feed(ip, port):
    try:
        video = CameraStreamer(ip, port)
    except Exception as e:
        flash(f'Error establishing video feed: {str(e)}', 'alert-danger')
        return redirect(url_for('main.index'))

    return Response(video.establish_connection(), mimetype='multipart/x-mixed-replace; boundary=frame')
