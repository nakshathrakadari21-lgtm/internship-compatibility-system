document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('compatibilityForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            // 1. Intercept Submission
            e.preventDefault();

            // 2. Data Processing (JSON Safety Fallbacks)
            const skillsRaw = document.getElementById('skills')?.value || "";
            const cgpaInput = parseFloat(document.getElementById('cgpa')?.value) || 0.0;
            const interestInput = document.getElementById('interest')?.value || "";
            const domainInput = document.getElementById('domain')?.value || "";

            // 3. Dynamic UI Update: Loading State
            const submitBtn = document.getElementById('submitBtn');
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Calculating Compatibility...';
            submitBtn.disabled = true;

            try {
                // 4. The API Call
                const response = await fetch('http://127.0.0.1:5000/api/compatibility', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        skills: skillsRaw,
                        cgpa: cgpaInput,
                        interest: interestInput,
                        domain: domainInput
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP Error: ${response.status}`);
                }

                const data = await response.json();

                // 5. Rendering: Clear container
                resultsContainer.innerHTML = '';

                // Handle Empty Matches
                if (data.length === 0) {
                    resultsContainer.innerHTML = `
                        <div class="empty-state">
                            <h3 style="color: #64748b;">No compatible roles found</h3>
                            <p>Try adjusting your skills or raising your CGPA threshold.</p>
                        </div>
                    `;
                    return;
                }

                // Loop through array and build HTML dynamically
                data.forEach((match, index) => {
                    // Sorting is handled by backend, so index 0 is optimal
                    const isOptimal = index === 0;
                    const cardClass = isOptimal ? 'compatibility-card optimal-match' : 'compatibility-card';
                    const score = match.compatibility_score;

                    // Determine score color class
                    let scoreClass = 'low';
                    if (score > 85) scoreClass = 'good';
                    else if (score >= 50) scoreClass = 'avg';

                    // Prepare user skills for comparison
                    const userSkills = skillsRaw.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);

                    // Filter missing skills
                    const missingSkills = match.required_skills.filter(skill => !userSkills.includes(skill.toLowerCase()));

                    // Generate skill tags
                    const skillsHTML = missingSkills.length > 0
                        ? missingSkills.map(skill => `<li class="skill-tag">${skill}</li>`).join('')
                        : '<span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">You meet all skill requirements!</span>';

                    // 6. Template Literal
                    const cardHTML = `
                        <div class="${cardClass}" style="animation-delay: ${index * 0.1}s">
                            ${match.status ? `<div class="optimal-badge">${match.status}</div>` : ''}
                            
                            <div class="card-header">
                                <h3 class="role-title">${match.role}</h3>
                                <div class="score-badge ${scoreClass}">${score}%</div>
                            </div>
                            
                            <div class="card-bottom">
                                <span class="role-domain">Domain: ${match.domain}</span>
                                
                                <div class="skills-section">
                                    <span class="skills-label">Missing Skills</span>
                                    <ul class="skills-list">
                                        ${skillsHTML}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    `;

                    // Append card
                    resultsContainer.insertAdjacentHTML('beforeend', cardHTML);
                });

            } catch (error) {
                console.error('Fetch Error:', error);
                // 7. Error Handling
                resultsContainer.innerHTML = `
                    <div class="error-msg">
                        <h3>Connection Error</h3>
                        <p>Server is unreachable, or an error occurred while fetching your matches.</p>
                        <p style="font-size: 0.8rem; margin-top: 1rem; color: #7f1d1d; opacity: 0.8;">Check if Flask is running on port 5000</p>
                    </div>
                `;
            } finally {
                // Revert Loading State
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
});
