let courses = null;

function getCourses() {
    return fetch('/api/course_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json());
}

function listCourses(courses) {
    const courseList = document.getElementById('course-list');
    courseList.replaceChildren([])
    for (const course of courses) {
        courseList.appendChild(generateCourseElement(course));
    }
}

function generateCourseElement(course) {
    const img_url = course['ImageURL'] ?? "https://placehold.co/600x400?text=No+Image";
    const template = document.createElement('template');
    template.innerHTML = `
    <div class="col">
        <a href="/course/${course['ID']}">
        <div class="card h-100 course-card">
            <img class="course-img" src="${img_url}" alt="Course image">
            
            <!-- Number of registered users -->
            <span class="img-text" style="top: 10px; left: 10px; border-radius: 3px;">
                ${course['Registrations']}
            </span>
            
            ${course['Rating'] == null ? "" : `
            <!-- Rating in the top-right corner -->
            <span class="img-text" style="top: 10px; right: 10px; border-radius: 3px;">
                ${course['Rating'] / 2} ⭐
            </span>`
            }
            
            <!-- Title at the bottom over the image -->
            <div class="img-text bottom-0 start-0 end-0">
                <p class="m-0" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    ${course['Title']}
                </p>
                <p class="m-0" style="font-size: 0.70rem;">
                    ${course['Code']}
                </p>
            </div>
        </div>
        </a>
    </div>
    `;
    return template.content.firstElementChild;
}


function filterCourses() {
    if (courses == null) return;
    const searchBar = document.getElementById('search-bar');
    const input = searchBar.value.toLowerCase();
    const filteredCourses = courses.filter(
        course => (
            course['Title'].toLowerCase().includes(input) ||
            course['Code'].toLowerCase().includes(input)
        )
    );
    listCourses(filteredCourses);
}

function initialize() {
    const searchBar = document.getElementById('search-bar');
    searchBar.oninput = filterCourses;
    
    getCourses().then(c => {
        courses = c;
        filterCourses();
    });
}

initialize();
