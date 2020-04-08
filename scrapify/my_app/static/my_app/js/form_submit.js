function onLoadSubmit() {
    document.formsubmit.submit();
}

function updateProgress(progressBarElement, progressBarMessageElement, progress) {
    progressBarElement.style.width = progress.percent + "%";
    progressBarMessageElement.innerHTML = progress.current + ' of ' + progress.total + ' processed.';
}

document.addEventListener("DOMContentLoaded", function () {
  var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
  CeleryProgressBar.initProgressBar(progressUrl);
});