function change_theme() {

    if (document.getElementById('body').classList.contains("light-blue")) {
        document.getElementById('body').classList.remove("light-blue");
        document.getElementById('fake-review-image').classList.remove("light-blue-box");
        //document.getElementById('try-button').classList.remove("light-blue-button");

        document.getElementById('body').classList.add("light-green");
        document.getElementById('fake-review-image').classList.add("light-green-box");
        //document.getElementById('try-button').classList.add("light-green-button");

    } else if (document.getElementById('body').classList.contains("light-green")) {
        document.getElementById('body').classList.remove("light-green");
        document.getElementById('fake-review-image').classList.remove("light-green-box");
        //document.getElementById('try-button').classList.remove("light-green-button");

        document.getElementById('body').classList.add("light-gray");
        document.getElementById('fake-review-image').classList.add("light-gray-box");
        //document.getElementById('try-button').classList.add("light-gray-button");

    } else if (document.getElementById('body').classList.contains("light-gray")) {
        document.getElementById('body').classList.remove("light-gray");
        document.getElementById('fake-review-image').classList.remove("light-gray-box");
        //document.getElementById('try-button').classList.remove("light-gray-button");

        document.getElementById('body').classList.add("light-blue");
        document.getElementById('fake-review-image').classList.add("light-blue-box");
        //document.getElementById('try-button').classList.add("light-blue-button");

    }
}