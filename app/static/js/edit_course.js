async function SaveChanges() {
    const title = document.getElementById('course_title').value;
    const code = document.getElementById('course_code').value;
    const description = document.getElementById('course_description').value;

    await fetch('/api/edit_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            course_id: course_id,
            title: title,
            code: code,
            description: description
        })
    })
    .then(response => { if (response.ok) {  } else { alert("Could not edit course.");} });

    const sessions = document.getElementById('sessions').children;  
    await addNewProfessors(sessions); 

    for (const session of sessions) {
        await saveSession(session);
    }

    for (const id of deleted_sessions) {
        await fetch('/api/delete_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({session_id: id})
        });
    }

    deleted_sessions = []

    await saveSections();
    await saveImage();

    location.reload();
}

function saveImage() {
    if (!imageChanged) return;

    const formData = new FormData();
    formData.append('course_id', course_id);
    if (window.img_file) formData.append('file', window.img_file);

    return fetch('/api/upload_course_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()).then(response => console.log(response));
}

async function addNewProfessors(sessions) {
    let professors = [];
    for (const session of sessions) {
        if (session.querySelector('.professor-select').value != 'new') continue;
        const fname = session.querySelector('.fn-input').value;
        const lname = session.querySelector('.ln-input').value;
        let added=false;
        for (const [fn, ln] of professors) {
            added |= (fn == fname) && (ln == lname);
        }

        if (!added) {
            professors.push([fname, lname]);
        }
    }
    
    for (let i=0; i<professors.length; i++) {
        const [fname, lname] = professors[i];
        await fetch('/api/add_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({first_name: fname, last_name: lname})
        })
        .then(response => response.json()).then(response => professors[i] = [fname, lname, response.new_id]);
    }

    await getProfessors();

    for (const session of sessions) {
        if (session.querySelector('.professor-select').value != 'new') continue;
        const fname = session.querySelector('.fn-input').value;
        const lname = session.querySelector('.ln-input').value;
        let added=false;
        for (const [fn, ln, id] of professors) {
            if ((fname == fn) && (lname == ln)) {
                session.querySelector('.professor-select').value = id;
                professorSelected(session.querySelector('.professor-select'));
            }
        }
    }
}

function saveSession(sessionElement) {
    const sessionData = {
        course_id: course_id,
        session_id: sessionElement.getAttribute('session-id'),
        title: sessionElement.querySelector('.title-input').value, 
        professor_id: sessionElement.querySelector('.professor-select').value,
        classroom: sessionElement.querySelector('.class-input').value,
        start_date: sessionElement.querySelector('.sd-input').value,
        end_date: sessionElement.querySelector('.ed-input').value,
        time: sessionElement.querySelector('.time-input').value,
        description: sessionElement.querySelector('.description-input').value
    };

    const addr = sessionData.session_id == -1 ? '/api/add_session' : '/api/edit_session';

    return fetch(addr, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sessionData)
    })
    .then(response => response.json()).then(response => console.log(response));
}

function professorSelected(select) {
    const newProf = select.value == "new";
    select.parentElement.nextElementSibling.classList.remove('d-none');
    if (select.value != "new") {
        select.parentElement.nextElementSibling.classList.add('d-none');
    }
}

async function saveSections() {
    const sectionElements = document.getElementById('sections').children; 

    for (const sectionElement of sectionElements) {
        const section_data = {
            course_id: course_id,
            section_id: sectionElement.getAttribute('section-id'),
            title: sectionElement.querySelector('.title-input').value, 
            page_id: sectionElement.querySelector('.page-input').value,
        };

        const addr = section_data.section_id == -1 ? '/api/add_section' : '/api/edit_section';

        await fetch(addr, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(section_data)
        })
        .then(response => response.json()).then(response => console.log(response));
    }

    for (const id of deleted_sections) {
        await fetch('/api/delete_section', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({section_id: id})
        }).then(response => response.json()).then(response => console.log(response));
    }

    deleted_sections = []
}

function addSession(session) {
    const sessions = document.getElementById('sessions');
    const template = document.createElement('template');
    template.innerHTML = `
    <div class="card mb-3" session-id="${session['ID'] ?? -1}">
        <div class="card-body">
            <div class="mb-2">
                <input type="text" placeholder="Session Title" class="form-control title-input" value="${session['Title'] ?? ""}" autofocus>
            </div>
            <div class="mb-2">
                <select class="form-select professor-select" onchange="professorSelected(this)">
                    <option selected>Select Professor</option>
                    <option>Add Professor</option>
                </select>
            </div>
            <div class="d-flex w-100 mb-2 d-none">
                <input type="text" placeholder="First Name" class="form-control me-2 fn-input" value="" autofocus>
                <input type="text" placeholder="Last Name" class="form-control ln-input" value="" autofocus>
            </div>
            <div class="d-flex w-100 mb-2">
                <input type="text" placeholder="Classroom" class="form-control me-2 class-input" value="${session['Classroom'] ?? ""}" autofocus>
                <input type="text" placeholder="Time" class="form-control time-input" value="${session['Time'] ?? ""}" autofocus>
            </div>
            <div class="d-flex w-100 mb-2">
                <input type="date" class="form-control me-2 sd-input" value="${session['StartDate'] ?? ""}" autofocus>
                <input type="date" class="form-control ed-input" value="${session['EndDate'] ?? ""}" autofocus>
            </div>
            <div class="mb-3">
                <textarea id="course_description" class="form-control description-input" placeholder="Description">${session['Description'] ?? ""}</textarea>
            </div>
            <button class="btn btn-danger" onclick="deleteSession(this)">Delete</button>
        </div>
    </div>
    `;
    const sessionHtml = template.content.firstElementChild;
    updateProfessorDropdown(sessionHtml.querySelector('.professor-select'));
    sessionHtml.querySelector('.professor-select').value = session['ProfessorID'] ?? 'select';

    sessions.appendChild(sessionHtml);
}

function addSection(section) {
    const sections = document.getElementById('sections');
    const template = document.createElement('template');
    template.innerHTML = `
    <div class="card mb-3" section-id="${section['ID'] ?? -1}">
        <div class="card-body p-2">
            <div class="d-flex justify-content-between">
                <input type="text" placeholder="Section Name" class="form-control title-input me-2" value="${section['Title'] ?? ""}" autofocus>
                <input type="text" placeholder="Page ID" class="form-control page-input me-2" value="${section['PageID'] ?? ""}" autofocus>
                <button class="btn btn-danger" onclick="deleteSection(this)">X</button>
            </div>
        </div>
    </div>
    `;
    sections.appendChild(template.content.firstElementChild);
}

function deleteSection(button) {
    const section = button.closest('.card');
    const section_id = section.getAttribute('section-id');
    section.parentElement.removeChild(section);
    if (section_id != "-1") {
        window.deleted_sections.push(Number(section_id));
    }
}

function deleteSession(button) {
    const session = button.closest('.card');
    const session_id = session.getAttribute('session-id');
    session.parentElement.removeChild(session);

    if (session_id != "-1") {
        window.deleted_sessions.push(Number(session_id));
    }
}

function updateProfessorDropdown(dropdown) {
    const current = dropdown.value;
    dropdown.replaceChildren([]);

    const defaultOption = document.createElement('option');
    defaultOption.value = 'select';
    defaultOption.innerText = "Select Professor";
    dropdown.appendChild(defaultOption);
    
    const newProfessorOption = document.createElement('option');
    newProfessorOption.value = 'new';
    newProfessorOption.innerText = "New Professor";
    dropdown.appendChild(newProfessorOption);

    for (const professor of professors) {
        const option = document.createElement('option');
        option.value = professor['ID'];
        option.innerHTML = `${professor['FirstName']} ${professor['LastName']}`;
        dropdown.appendChild(option);
    }
    dropdown.value = current;
    professorSelected(dropdown);
}

function updateProfessorDropdowns() {
    const selects = document.getElementsByClassName('professor-select');
    for (const select of selects) {
        updateProfessorDropdown(select);
    }
}

function getProfessors() {
    return fetch('/api/get_professors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(professors => {
        window.professors = professors;
        updateProfessorDropdowns(professors);
    });
}

function getSessions() {
    return fetch('/api/get_sessions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({course_id: window.course_id })
    })
    .then(response => response.json())
    .then(sessions => {
        for (const session of sessions) {
            addSession(session);
        }
    });
}

function getSections() {
    return fetch('/api/get_sections', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({course_id: window.course_id})
    })
    .then(response => response.json())
    .then(sections => {
        for (const section of sections) {
            addSection(section);
        }
    });
}

function imageSelected() {
    const imageInput = document.getElementById("profilePicture");
    const preview = document.getElementById('profilePreview');

    if (imageInput.files.length === 0) {
    } else {
        window.imageChanged = true;
        const file = imageInput.files[0];
        const image = document.createElement("img");
        preview.src = URL.createObjectURL(file);
        window.img_file = file;
    }
}

function resetImage() {
    window.imageChanged = false;
    window.img_file = null;
    const preview = document.getElementById('profilePreview');
    preview.src = window.img_url.length > 0 ? window.img_url : "https://placehold.co/600x400?text=No+Image";
}

function clearImage() {
    window.imageChanged = true;
    window.img_file = null;
    const preview = document.getElementById('profilePreview');
    preview.src = "https://placehold.co/600x400?text=No+Image";
}

async function initialize() {
    window.professors = [];
    window.deleted_sessions = [];
    window.deleted_sections = [];
    window.img_file = null;

    await getProfessors();
    await getSessions();
    await getSections();

    const imageInput = document.getElementById("profilePicture");
    imageInput.addEventListener("change", imageSelected);
    window.imageChanged = false;
}

initialize();