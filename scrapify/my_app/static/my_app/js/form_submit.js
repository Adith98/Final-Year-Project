function onLoadSubmit() {
    document.formsubmit.submit();
}

function updateProgress(progressBarElement, progressBarMessageElement, progress) {
    progressBarElement.style.width = progress.percent + "%";
    progressBarMessageElement.innerHTML = progress.current + ' of ' + progress.total + ' processed.';
}

