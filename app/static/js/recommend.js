const questions = [
  {
    key: "interest",
    prompt: "What topic are you interested in?",
    options: ["AI", "Web Development", "Data Science", "Cybersecurity", "Cloud Computing"]
  },
  {
    key: "level",
    prompt: "What is your current skill level?",
    options: ["Beginner", "Intermediate", "Advanced"]
  },
  {
    key: "language",
    prompt: "Preferred course language?",
    options: ["English", "Hindi", "Spanish", "Not Specific"]
  }
];

let answers = {};
let current = 0;

const container = document.getElementById("question-container");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const searchInput = document.getElementById("search-input");
const searchResult = document.getElementById("search-result");

function askQuestion() {
  if (current >= questions.length) {
    fetchStructuredRecommendations();
    return;
  }

  const q = questions[current];
  const div = document.createElement("div");
  div.className = "question active";

  let optionsHTML = `<label>${q.prompt}</label><br><select onchange="captureAnswer(this)">`;
  optionsHTML += `<option value="">Select...</option>`;
  for (let opt of q.options) {
    optionsHTML += `<option value="${opt}">${opt}</option>`;
  }
  optionsHTML += `</select>`;

  div.innerHTML = optionsHTML;
  container.innerHTML = "";
  container.appendChild(div);

  setTimeout(() => div.classList.add("active"), 10);
}

function captureAnswer(select) {
  const value = select.value;
  if (value) {
    answers[questions[current].key] = value;
    current++;
    askQuestion();
  }
}

async function fetchStructuredRecommendations() {
  container.innerHTML = "";
  result.innerHTML = "";
  loading.innerHTML = `Loading recommendations...`;

  try {
    const res = await fetch("/recommend_courses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(answers)
    });

    const data = await res.json();
    loading.innerHTML = "";

    result.innerHTML = `<h3>Recommended Courses:</h3><ul>` +
      data.map(course => `<li><a href="${course.url}" target="_blank">${course.title}</a></li>`).join("") +
      `</ul>`;
  } catch (error) {
    loading.innerHTML = "Something went wrong.";
    console.error(error);
  }
}

async function submitSearch() {
  const query = searchInput.value.trim();
  if (!query) return;

  searchResult.innerHTML = "Searching...";
  const res = await fetch("/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });

  const data = await res.json();
  searchResult.innerHTML = `<h3>Search Results:</h3><ul>` +
    data.map(course => `<li><a href="${course.url}" target="_blank">${course.title}</a></li>`).join("") +
    `</ul>`;
}
askQuestion();


// Search Box
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('search_field');
    input.oninvalid = function(event) {
        event.target.setCustomValidity('Please enter a field name (e.g. Python, Java, MySQL, etc.)');
    };
    input.oninput = function(event) {
        event.target.setCustomValidity('');
    };
});
