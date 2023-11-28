from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from system.camera import CameraStreamer

from . import main_bp
from .form import ManualConfigForm
from .models import Device

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ManualConfigForm(request.form)

    if form.validate_on_submit():
        d_name = form.device_name.data
        d_type = form.device_type.data
        ip = form.ip_address.data

        new_device = Device(d_name, d_type, ip)

        existing_device = Device.get_by_ip(new_device.ip_address)
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

    devices = Device.get_all_devices()
    return render_template('main/index.html', form=form, devices=devices)

@main_bp.route('/device/<int:device_id>', methods=['GET', 'POST'])
@login_required
def device_view(device_id):
    device = Device.get_by_id(device_id)

    return render_template('main/device_view.html', device=device)