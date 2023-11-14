// custom.js
// 自動關閉 alert 訊息框
function autoCloseAlert() {
  var alertElement = document.querySelector('.alert');
  if (alertElement) {
    setTimeout(function () {
      alertElement.remove();
    }, 5000); // 5 秒後自動關閉
  }
}

autoCloseAlert(); // 載入頁面後啟動自動關閉功能
