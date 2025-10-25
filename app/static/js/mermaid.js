import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
// import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";


// inilializing model for default diagram
mermaid.initialize({
    startOnLoad: true,
    theme: "default",
    securityLevel: "loose",
    actionButtons: {
        enabled: true,
        download: true,
        copy: true
    }
});


// dynamic flowcharts
document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById("generate");
    const queryInput = document.getElementById("userQuery");
    const defaultDiagram = document.getElementById("defaultDiagram");
    const diagramContainer = document.getElementById("diagram");
    const diagramContent = document.getElementById("diagram_content");
    const diagramWrapper = document.getElementById("diagram_wrapper");
    const statusDiv = document.getElementById("status");
    const downloadBtn = document.getElementById("downloadBtn");
    const shareBtn = document.getElementById("shareBtn");
    shareBtn.disabled = true;
    let lastQuery = "";
    let currentRoadmapId = null;

    async function generateDiagram(query){
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
            currentRoadmapId = data.roadmap_id;
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
            const uniqueId = `flowchart${currentRoadmapId}`;
            const { svg } = await mermaid.render(uniqueId, mermaidCode);
            diagramContainer.style.display = "block";
            diagramContent.innerHTML = svg;
            statusDiv.innerHTML = "";
            shareBtn.disabled = false;

        } catch (err) {
            console.error("Error generating diagram", err);
            statusDiv.innerHTML = `<span style="font-size:1rem;">⚠️ Failed to generate...Try again</span>`;
        }
    };
    
    // Toggle Generate button
    queryInput.addEventListener("input", () => {
        const query = queryInput.value.trim();

        if (!query) {
            generateBtn.textContent = "Generate";
        } 
        else if (query !== lastQuery.trim()) {
            generateBtn.textContent = "Generate";
        } 
        else {
            generateBtn.textContent = "Regenerate";
        }
    });

    generateBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const query = queryInput.value.trim();
        if (!query) {
            statusDiv.innerHTML = `<span font-size:2rem;">⚠️Please describe your roadmap</span>`;
            return;
        }
        if (query.length < 15) {
            statusDiv.innerHTML = `<span style="color:red; font-size:1rem;">⚠️Query must be atleast 15 characters long</span>`;
            return;
        }

        lastQuery = query;
        generateBtn.disabled = true;
        await generateDiagram(lastQuery);
        generateBtn.disabled = false;
        generateBtn.textContent = "Regenerate";
    });

    // download feature 
    downloadBtn.addEventListener("click", () => {
        const svgElement = diagramContainer.querySelector("svg");
        if (!svgElement) {
            alert("No diagram to download...");
            return;
        }
        const serializer = new XMLSerializer();
        const svgBlob = new Blob([serializer.serializeToString(svgElement)], {type: "image/svg+xml"});
        const url = URL.createObjectURL(svgBlob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `roadmap_diagram${Date.now()}.svg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    shareBtn.addEventListener("click", () => {
        if (!currentRoadmapId) {
            alert("No roadmap generated yet...");
            return;
        }
        const link = `${window.location.origin}/roadmap_view/${currentRoadmapId}`;
        navigator.clipboard.writeText(link).then(() => {
            alert("Roadmap link copied !");
        });
    });


    // scroll zoom-in/out feature:-
    let scale = 1;
    let isPanning = false;
    let startX, startY, scrollLeft, scrollTop;

    diagramWrapper.addEventListener("wheel", (e) => {
            e.preventDefault();

            if (e.deltaY < 0) {
                scale *= 1.1;
            } else {
                scale /= 1.1;
            }
            // limit zoom range
            scale = Math.min(Math.max(scale, 0.3), 3);
            diagramContent.style.transform = `scale(${scale})`;
    });
    diagramWrapper.addEventListener("mousedown", (e) => {
        isPanning = true;
        diagramWrapper.classList.add("no-select");
        diagramWrapper.style.cursor = "grabbing";
        startX = e.pageX - diagramWrapper.offsetLeft;
        startY = e.pageY - diagramWrapper.offsetTop;
        scrollLeft = diagramWrapper.scrollLeft;
        scrollTop = diagramWrapper.scrollTop;
    });
    diagramWrapper.addEventListener("mousemove", (e) => {
        if (!isPanning) return;
        e.preventDefault();
        const x = e.pageX - diagramWrapper.offsetLeft;
        const y = e.pageY - diagramWrapper.offsetTop;
        const walkX = (x - startX);
        const walkY = (y - startY);
        diagramWrapper.scrollLeft = scrollLeft - walkX;
        diagramWrapper.scrollTop = scrollTop - walkY;
    });
    diagramWrapper.addEventListener("mouseup", () => {
        isPanning = false;
        diagramWrapper.classList.remove("no-select");
        diagramWrapper.style.cursor = "grab";
    });
    diagramWrapper.addEventListener("mouseleave", () => {
        isPanning = false;
        diagramWrapper.classList.remove("no-select");
        diagramWrapper.style.cursor = "grab";
    });

})