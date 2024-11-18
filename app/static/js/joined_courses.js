document.addEventListener("DOMContentLoaded", () => {
    const joinedCourseList = document.getElementById("joined-course-list");
    const searchBar = document.getElementById("search-bar-joined");

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
        joinedCourseList.innerHTML = "";

        if (courses.length === 0) {
            joinedCourseList.innerHTML = "<p class='text-muted'>No joined courses found.</p>";
            return;
        }

        courses.forEach(course => {
            const courseCard = document.createElement("div");
            courseCard.classList.add("col");

            courseCard.innerHTML = `
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">${course.Title} (${course.Code})</h5>
                        <p class="card-text">Joined on: ${course.JoinDate}</p>
                        <small>Last viewed: ${course.ViewDate}</small>
                    </div>
                </div>
            `;

            joinedCourseList.appendChild(courseCard);
        });
    }

    // Filter courses based on search input
    searchBar.addEventListener("input", (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const courseCards = joinedCourseList.querySelectorAll(".card");

        courseCards.forEach(card => {
            const title = card.querySelector(".card-title").textContent.toLowerCase();
            card.style.display = title.includes(searchTerm) ? "block" : "none";
        });
    });

    // Initial fetch of joined courses
    fetchJoinedCourses();
});
