
var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
  lineNumbers: true,
  mode:  "xml"
});

function submitHtml() {
  debugger;
  editor.save();
  var code = document.getElementById("editor").value;
  var data_url = "data:text/html;charset=utf-8;base64," + $.base64.encode(code);
  document.getElementById("result").src = data_url;
}

module.exports = {
  submitHtml: submitHtml,
};
