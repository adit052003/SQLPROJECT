document.addEventListener("DOMContentLoaded", () => {
    const joinedCourseList = document.getElementById("joined-course-list");

    // Fetch joined courses from the API
    async function fetchJoinedCourses() {
        try {
            const response = await fetch("/api/joined_courses");
            const data = await response.json();

            displayCourses(data.courses);
        } catch (error) {
            console.error("Error fetching joined courses:", error);
        }
    }

    // Display the list of joined courses
    function displayCourses(courses) {
        joinedCourseList.innerHTML = ""; // Clear existing content

        if (courses.length === 0) {
            joinedCourseList.innerHTML = "<p class='text-muted'>No dynamic joined courses found.</p>";
            return;
        }

        courses.forEach(course => {
            const courseCard = document.createElement("div");
            courseCard.classList.add("col-md-4", "mb-4");

            courseCard.innerHTML = `
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">${course.Title} (${course.Code})</h5>
                        <p class="card-text">Joined on: ${course.JoinDate}</p>
                        <small>Last viewed: ${course.ViewDate}</small>
                        <a href="/course/${course.ID}" class="btn btn-primary mt-3">View Course</a>
                    </div>
                </div>
            `;

            joinedCourseList.appendChild(courseCard);
        });
    }

    // Initial fetch of joined courses
    fetchJoinedCourses();
});
