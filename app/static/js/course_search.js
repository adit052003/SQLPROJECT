let courses = null;


function getCourses() {
    return fetch('/api/course_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        return data.courses;
    });
}

function listCourses(courses) {
    const courseList = document.getElementById('course-list');
    courseList.replaceChildren([])
    for (const course of courses) {
        courseList.appendChild(generateCourseElement(course));
    }
}

function generateCourseElement(course) {
    const template = document.createElement('template');
    template.innerHTML = `
    <div class="col">
        <a href="/course/${course.id}">
        <div class="card h-100 course-card">
            <img class="course-img" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Iglesia_de_Nuestra_Se%C3%B1ora_de_La_Blanca%2C_Cardej%C3%B3n%2C_Espa%C3%B1a%2C_2012-09-01%2C_DD_02.JPG/550px-Iglesia_de_Nuestra_Se%C3%B1ora_de_La_Blanca%2C_Cardej%C3%B3n%2C_Espa%C3%B1a%2C_2012-09-01%2C_DD_02.JPG" alt="Course image">
            
            <!-- Number of registered users -->
            <span class="img-text" style="top: 10px; left: 10px; border-radius: 3px;">
                ${course.registrations}
            </span>
            
            ${course.rating == null ? "" : `
            <!-- Rating in the top-right corner -->
            <span class="img-text" style="top: 10px; right: 10px; border-radius: 3px;">
                ${course.rating / 2} ⭐
            </span>`
            }
            
            <!-- Title at the bottom over the image -->
            <div class="img-text bottom-0 start-0 end-0">
                <p class="m-0" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    ${course.title}
                </p>
                <p class="m-0" style="font-size: 0.70rem;">
                    ${course.code}
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
            course.title.toLowerCase().includes(input) ||
            course.code.toLowerCase().includes(input)
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
