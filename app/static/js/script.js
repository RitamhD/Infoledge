import { startScheduledRefresh } from "./jwt_auth.js";

window.addEventListener("DOMContentLoaded", () => {
    startScheduledRefresh(25);
    
    
    function playVideo(container){
        const video = container.querySelector('video');
        if (video){
            video.play();
        }
    }
    
    function pauseVideo(container){
        const video = container.querySelector('video');
        if (video){
            video.pause();
        }
    }
    
    const contentOptions = document.getElementsByClassName('content_options');
    
    Array.from(contentOptions).forEach(container => {
        container.addEventListener('mouseenter', () => playVideo(container));
        container.addEventListener('mouseleave', () => pauseVideo(container));
    })
});


// var editorPython = CodeMirror.fromTextArea(document.getElementById('editor'), {
//     name: "python",
//     version: 3,
//     theme: "dracula",
//     lineNumbers: true,
//     defaultTextHeight: 10,
//     autoCloseBrackets: true,
//     indentWithTabs: true,
//     smartIndent: false,
// }); 
// var editorCpp = CodeMirror.fromTextArea(document.getElementById('editor'), {
//     mode: "text/x-c++src",
//     theme: "dracula",
//     lineNumbers: true,
//     autoCloseBrackets: true
// });

// var editorJava = CodeMirror.fromTextArea(document.getElementById('editor'), {
//     mode: "text/x-java",
//     theme: "dracula",
//     lineNumbers: true,
//     autoCloseBrackets: true
// });

// var width = window.innerWidth;
// editorPython.setSize(0.7*width, "600");
// editorCpp.setSize(0.7*width, "600")
// editorJava.setSize(0.7*width, "600")


// let defaultText = "#---Let's code---\nprint('Hello World!')";
// let blankLines = '\n'.repeat(5);
// editorPython.getWrapperElement().style.fontSize = '16px';
// editorPython.setValue(defaultText+blankLines);


// // Select all buttons with the class 'playButton'
// document.querySelectorAll('.playButton').forEach(function(button) {
//     button.addEventListener('click', function() {
//         const videoId = this.getAttribute('data-video-id'); // Get video ID from the button's 'data-video-id' attribute
        
//         // Create the iframe element for YouTube
//         const iframe = document.createElement('iframe');
//         iframe.width = '560';
//         iframe.height = '315';
//         iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`; // Autoplay the video when the iframe is created
//         iframe.frameBorder = '0';
//         iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
//         iframe.allowFullscreen = true;

//         // Find the container to append the iframe
//         const container = document.getElementById('videoContainer');
//         container.innerHTML = ''; // Clear any previous videos
//         container.appendChild(iframe); // Append the iframe to the container
//     });
// });


