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
                if (!data || Object.keys(data).length === 0) {
                    resultsContainer.innerHTML = `
                        <div class="empty-state">
                            <h3 style="color: #64748b;">No compatible roles found</h3>
                            <p>Try adjusting your skills or raising your CGPA threshold.</p>
                        </div>
                    `;
                    return;
                }

                const score = data.score;
                let scoreColor = '#ef4444'; // Red
                let progressColor = '#fee2e2';
                if (score >= 80) { scoreColor = '#10b981'; progressColor = '#dcfce7'; }
                else if (score >= 50) { scoreColor = '#f59e0b'; progressColor = '#fef3c7'; }

                const missingSkillsHTML = data.missing_skills.length > 0
                    ? data.missing_skills.map(s => `<li class="skill-tag">⚠️ <span>${s}</span></li>`).join('')
                    : `<li class="skill-tag success">✔️ No missing skills!</li>`;

                const recsHTML = data.recommendations.length > 0
                    ? data.recommendations.map(r => `<li class="rec-item">✔️ ${r}</li>`).join('')
                    : `<li class="rec-item">✔️ Keep up the great work!</li>`;

                const topMatchesHTML = data.top_matches.map(m => `
                    <li class="match-card">
                        <div class="match-header">
                            <span class="match-role">⭐ ${m.role}</span>
                            <span class="match-score" style="color: ${m.score >= 80 ? '#10b981' : (m.score >= 50 ? '#f59e0b' : '#ef4444')}">${m.score}%</span>
                        </div>
                        ${m.missing_skills.length > 0 
                            ? `<div class="match-skills">Missing Skills: ${m.missing_skills.join(', ')}</div>` 
                            : `<div class="match-skills success">✔️ No missing skills!</div>`}
                    </li>`).join('');

                const cardHTML = `
                    <div class="skill-gap-card">
                        <div class="sg-header">
                            <div class="sg-title">
                                <span class="student-name">Student Analysis</span>
                                <h2>${data.role}</h2>
                            </div>
                            <!-- Circular progress via conic-gradient -->
                            <div class="circular-progress" style="background: conic-gradient(${scoreColor} ${score}%, ${progressColor} 0);">
                                <div class="inner-circle"><span class="score-text" style="color: ${scoreColor};">${score}%</span></div>
                            </div>
                        </div>

                        <div class="sg-section">
                            <h4>Interest Match</h4>
                            <div style="margin-top: 0.5rem; display: flex; flex-direction: column; gap: 0.75rem;">
                                <div class="interest-box ${data.interest_status === 'Exact Match' ? 'success' : (data.interest_status === 'Partial Match' ? 'warning' : 'error')}">
                                    <span>${data.interest_status === 'Exact Match' ? '✅' : (data.interest_status === 'Partial Match' ? '⚠️' : '❌')} ${data.interest_status}</span>
                                </div>
                                <p style="font-size: 0.85rem; margin: 0;">${data.interest_reason}</p>
                            </div>
                        </div>

                        <div class="sg-section">
                            <h4>Missing Skills</h4>
                            <ul class="tags-list">
                                ${missingSkillsHTML}
                            </ul>
                        </div>

                        <div class="sg-section">
                            <h4>Recommendations</h4>
                            <ul class="emoji-list">
                                ${recsHTML}
                            </ul>
                        </div>

                        <div class="sg-section">
                            <h4>Top Matches</h4>
                            <ul class="emoji-list">
                                ${topMatchesHTML}
                            </ul>
                        </div>
                    </div>
                `;

                resultsContainer.innerHTML = cardHTML;

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
