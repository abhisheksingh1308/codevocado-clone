function toggleMenu() {
  const menu = document.getElementById("navMenu");
  menu.classList.toggle("active");
}

const reveals = document.querySelectorAll(".reveal");
window.addEventListener("scroll", () => {
  reveals.forEach(el => {
    if (el.getBoundingClientRect().top < window.innerHeight - 100) {
      el.classList.add("active");
    }
  });
});

// Modal Functions
function openDemoModal() {
  const modal = document.getElementById("demoModal");
  if (modal) modal.style.display = "block";
}

function closeDemoModal() {
  const modal = document.getElementById("demoModal");
  if (modal) modal.style.display = "none";
}

function openCreateTestModal() {
  const modal = document.getElementById("createTestModal");
  if (modal) modal.style.display = "block";
}

function closeCreateTestModal() {
  const modal = document.getElementById("createTestModal");
  if (modal) modal.style.display = "none";
}

function openForgotPasswordModal() {
  const modal = document.getElementById("forgotPasswordModal");
  if (modal) modal.style.display = "block";
}

function closeForgotPasswordModal() {
  const modal = document.getElementById("forgotPasswordModal");
  if (modal) modal.style.display = "none";
}

// Close modal when clicking outside
window.onclick = function(event) {
  const demoModal = document.getElementById("demoModal");
  const createModal = document.getElementById("createTestModal");
  const forgotModal = document.getElementById("forgotPasswordModal");
  
  if (event.target == demoModal) {
    demoModal.style.display = "none";
  }
  if (event.target == createModal) {
    createModal.style.display = "none";
  }
  if (event.target == forgotModal) {
    forgotModal.style.display = "none";
  }
}

// Dynamic Question Adding
let questionCount = 0;

function addQuestion() {
    questionCount++;
    const container = document.getElementById('questionsContainer');
    const div = document.createElement('div');
    div.className = 'question-card';
    div.innerHTML = `
        <div class="question-header">
            <h4>Question ${questionCount}</h4>
            <button type="button" class="btn-sm btn-danger" onclick="this.parentElement.parentElement.remove()">Remove</button>
        </div>
        <div class="form-group">
            <label>Question Text</label>
            <input type="text" name="question_text_${questionCount}" required placeholder="Enter question">
        </div>
        <div class="options-grid">
            <div class="form-group">
                <label>Option A</label>
                <input type="text" name="option_a_${questionCount}" required>
            </div>
            <div class="form-group">
                <label>Option B</label>
                <input type="text" name="option_b_${questionCount}" required>
            </div>
            <div class="form-group">
                <label>Option C</label>
                <input type="text" name="option_c_${questionCount}" required>
            </div>
            <div class="form-group">
                <label>Option D</label>
                <input type="text" name="option_d_${questionCount}" required>
            </div>
        </div>
        <div class="form-group">
            <label>Correct Answer</label>
            <select name="correct_option_${questionCount}" required>
                <option value="A">Option A</option>
                <option value="B">Option B</option>
                <option value="C">Option C</option>
                <option value="D">Option D</option>
            </select>
        </div>
    `;
    container.appendChild(div);
}

// Handle Create Test Form Submission
document.getElementById('createTestForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const questions = [];
    const questionCards = document.querySelectorAll('.question-card');
    
    // Extract questions manually since we used dynamic names
    questionCards.forEach((card, index) => {
        // Find inputs within this specific card
        const qIndex = index + 1; // Or find a more robust way if removing messes up indices
        // Better: iterate over inputs in the card
        const text = card.querySelector('input[name^="question_text"]').value;
        const optA = card.querySelector('input[name^="option_a"]').value;
        const optB = card.querySelector('input[name^="option_b"]').value;
        const optC = card.querySelector('input[name^="option_c"]').value;
        const optD = card.querySelector('input[name^="option_d"]').value;
        const correct = card.querySelector('select[name^="correct_option"]').value;
        
        questions.push({
            question_text: text,
            option_a: optA,
            option_b: optB,
            option_c: optC,
            option_d: optD,
            correct_option: correct
        });
    });
    
    const payload = {
        title: formData.get('title'),
        description: formData.get('description'),
        duration: formData.get('duration'),
        total_marks: formData.get('total_marks'),
        start_date: formData.get('start_date'),
        end_date: formData.get('end_date'),
        questions: questions
    };
    
    try {
        const response = await fetch('/create-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (response.status === 401) {
            alert('Your session has expired. Please login again.');
            window.location.href = '/login';
            return;
        }

        const result = await response.json();
        
        if (result.success) {
            alert('Assessment created successfully!');
            closeCreateTestModal();
            // Reload dashboard if on dashboard page
            if (window.location.pathname.includes('dashboard')) {
                loadAssessments();
            } else {
                window.location.href = '/dashboard';
            }
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while saving the assessment.');
    }
});

// Dashboard: Load Assessments
async function loadAssessments() {
    const tableBody = document.querySelector('#assessmentTable tbody');
    if (!tableBody) return; // Not on dashboard page
    
    try {
        const response = await fetch('/manage-assessments');
        
        if (response.status === 401) {
             window.location.href = '/login';
             return;
        }

        const data = await response.json();
        
        if (data.success) {
            tableBody.innerHTML = '';
            data.assessments.forEach(test => {
                const row = `
                    <tr>
                        <td>${test.title}</td>
                        <td>${new Date(test.start_date).toLocaleString()}</td>
                        <td>${test.duration} mins</td>
                        <td><span class="badge ${test.status}">${test.status}</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-sm" onclick="alert('View feature coming soon')">View</button>
                                <button class="btn-sm btn-outline" onclick="alert('Edit feature coming soon')">Edit</button>
                                ${test.status === 'draft' 
                                    ? `<button class="btn-sm btn-success" onclick="updateStatus(${test.id}, 'publish')">Publish</button>` 
                                    : `<button class="btn-sm btn-warning" onclick="updateStatus(${test.id}, 'unpublish')">Unpublish</button>`
                                }
                                <button class="btn-sm btn-danger" onclick="deleteAssessment(${test.id})">Delete</button>
                            </div>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        }
    } catch (error) {
        console.error('Error loading assessments:', error);
    }
}

// Dashboard: Update Status / Delete
async function updateStatus(id, action) {
    if (!confirm(`Are you sure you want to ${action} this assessment?`)) return;
    
    try {
        const response = await fetch(`/assessment/${id}/${action}`, { method: 'POST' });
        
        if (response.status === 401) {
            alert('Your session has expired. Please login again.');
            window.location.href = '/login';
            return;
        }

        const result = await response.json();
        
        if (result.success) {
            loadAssessments();
            showAlert(result.message, 'success');
        } else {
            showAlert(result.message, 'error');
        }
    } catch (error) {
        showAlert('An error occurred', 'error');
    }
}

async function deleteAssessment(id) {
    updateStatus(id, 'delete');
}

function showAlert(message, type) {
    const alertDiv = document.getElementById('dashboardAlert');
    if (alertDiv) {
        alertDiv.textContent = message;
        alertDiv.className = `alert alert-${type}`;
        alertDiv.style.display = 'block';
        setTimeout(() => alertDiv.style.display = 'none', 3000);
    } else {
        alert(message);
    }
}
