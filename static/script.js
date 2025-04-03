
var editorPython = CodeMirror.fromTextArea(document.getElementById('editor'), {
    name: "python",
    version: 3,
    theme: "dracula",
    lineNumbers: true,
    autoCloseBrackets: true,
    indentWithTabs: true,
    smartIndent: false,
    // indentOnInput: true,
    // extraKeys: {
    //     "Enter": function(cm) {
    //         var cursor = cm.getCursor();
    //         var line = cm.getLine(cursor.line);
            
    //         // Check if the current line ends with a colon (for Python indentation style)
    //         if (line.trim().endsWith(":")) {
    //             // If so, insert a newline and indent it based on the previous line
    //             cm.execCommand("newlineAndIndent");
    //         } else {
    //             // Otherwise, just insert a newline without special indentation
    //             cm.execCommand("newlineAndIndentContinueSelection");
    //         }
    //     }
    // }
});

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

var width = window.innerWidth;
editorPython.setSize(0.7*width, "500");
// editorCpp.setSize(0.7*width, "500")
// editorJava.setSize(0.7*width, "500")



























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


