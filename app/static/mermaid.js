import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
// import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";


// inilializing model for default diagram
mermaid.initialize({startOnLoad: true});


// dynamic flowcharts
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("flowForm");
    const defaultDiagram = document.getElementById("defaultDiagram");
    const diagramContainer = document.getElementById("diagram");
    const diagramContent = document.getElementById("diagram_content");
    const statusDiv = document.getElementById("status");

    form.addEventListener("submit", async function(e){
        e.preventDefault();

        let query = document.getElementById("userQuery").value;

        try{
            statusDiv.innerHTML = `
                <div class="dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
                <p>Generating your roadmap</p>
            `;
            
            diagramContent.innerHTML = "";

            const res = await fetch("/generate_roadmap", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({prompt: query})
            });

            if (! res.ok) {
                throw new Error(`Server error: ${res.status}`);
            }

            const data = await res.json();
            let mermaidCode = data.mermaid_code;
            mermaidCode = mermaidCode.replace(/```mermaid/g, "").replace(/```/g, "").trim();
            console.log("Rendering Mermaid:", mermaidCode);

            if(! mermaidCode) {
                throw new Error("No Mermaid code returned");
            }

            if (defaultDiagram) {
                defaultDiagram.innerHTML = "";
                defaultDiagram.style.display = "none";
            }

            // mermaid needs unique id for rendering everytime
            const uniqueId = `flowchart${Date.now()}`;
            const { svg } = await mermaid.render(uniqueId, mermaidCode);
            diagramContainer.style.display = "block";
            diagramContent.innerHTML = svg;
            statusDiv.innerHTML = "";

        } catch (err) {
            console.error("Error generating diagram", err);
            statusDiv.innerHTML = `<p style="color: red;">⚠️ Failed to generate... Try again</p>`;
        }
    })
})