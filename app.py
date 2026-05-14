from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key-development-only'
CORS(app)  # Enable CORS for frontend connection

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('home'))
        return render_template("login.html")
        
    email = request.form.get('email')
    password = request.form.get('password')
    
    print(f"Login attempt with email: {email}")
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        print("Login successful.")
        return redirect(url_for('home'))
        
    print("Invalid login attempt.")
    return render_template("login.html", error="Invalid email or password")

def get_db_connection():
    conn = sqlite3.connect('internships.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signup', methods=['POST'])
def api_signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
        
    hashed_kw = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_kw))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered"}), 409
    finally:
        conn.close()
        
    return jsonify({"success": True, "message": "Account created successfully"}), 201

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"}), 200

def normalize_string(s):
    if not s:
        return ""
    # Convert to lowercase and remove spaces and special characters
    s = s.lower().replace(" ", "").replace("/", "").replace("-", "")
    if s in ["webdevelopment", "webdev", "frontend", "ui", "ux"]:
        return "webdevelopment"
    elif s in ["backenddevelopment", "backend", "backenddev"]:
        return "backenddevelopment"
    elif s in ["datascience", "data"]:
        return "datascience"
    elif s in ["aiml", "ai", "machinelearning", "ml"]:
        return "aiml"
    elif s in ["cybersecurity", "security", "infosec"]:
        return "cybersecurity"
    elif s in ["cloudcomputing", "cloud"]:
        return "cloudcomputing"
    elif s in ["mobiledevelopment", "mobileapp", "mobiledev", "appdev"]:
        return "mobiledevelopment"
    elif s in ["softwaretesting", "qa", "testing"]:
        return "softwaretesting"
    return s

@app.route('/api/compatibility', methods=['POST'])
def compatibility():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400
            
        skills_raw = data.get('skills', "")
        if isinstance(skills_raw, list):
            skills_raw = ",".join(skills_raw)
            
        try:
            user_cgpa = float(data.get('cgpa', 0.0))
        except (ValueError, TypeError):
            return jsonify({"error": "CGPA must be a valid number"}), 400
            
        user_interest = data.get('interest', '').strip().lower()
        user_domain = data.get('domain', '').strip().lower()
        
        # Convert user_skills into a lowercase list
        user_skills = set([s.strip().lower() for s in skills_raw.split(',') if s.strip()])
        
        conn = get_db_connection()
        internships = conn.execute('SELECT * FROM internships').fetchall()
        conn.close()
        
        results = []
        for row in internships:
            req_min_cgpa = row['min_cgpa']
            
            # Step 1: The CGPA Hard-Filter
            if user_cgpa < req_min_cgpa:
                continue
                
            # Step 2: Skill Matching
            db_skills_raw = row['skills'].split(',')
            db_skills = set([s.strip().lower() for s in db_skills_raw if s.strip()])
            
            if len(db_skills) == 0:
                skill_score = 100.0
            else:
                matching_skills = user_skills.intersection(db_skills)
                skill_score = (len(matching_skills) / len(db_skills)) * 100
                
            # Step 3: CGPA Score
            cgpa_score = (user_cgpa / 10.0) * 100
            
            # Step 4: Interest & Domain Score
            norm_user_interest = normalize_string(user_interest)
            norm_user_domain = normalize_string(user_domain)
            norm_db_domain = normalize_string(row['domain'])
            role_title_lower = row['role'].lower()
            
            interest_score = 0.0
            interest_status = "No Match"
            interest_reason = "Your interest does not strongly align with this role."
            
            if (norm_user_interest and norm_user_interest == norm_db_domain) or (user_interest and user_interest in role_title_lower):
                interest_score = 100.0
                interest_status = "Exact Match"
                interest_reason = f"Your interest exactly matches the {row['domain']} domain or role title."
            else:
                user_i = user_interest.lower()
                if "full stack development" in user_i and ("ui" in role_title_lower or "backend" in role_title_lower):
                    interest_score = 50.0
                    interest_status = "Partial Match"
                    interest_reason = "Full Stack Development includes technologies relevant to UI/Backend Development."
                elif "web development" in user_i and ("ui" in role_title_lower or "frontend" in role_title_lower):
                    interest_score = 50.0
                    interest_status = "Partial Match"
                    interest_reason = "Web Development overlaps with Frontend and UI roles."
                elif "data science" in user_i and ("data analyst" in role_title_lower or "ai" in role_title_lower):
                    interest_score = 50.0
                    interest_status = "Partial Match"
                    interest_reason = "Data Science shares core concepts with Data Analysis and AI."
                elif "ai/ml" in user_i and "ai engineer" in role_title_lower:
                    interest_score = 50.0
                    interest_status = "Partial Match"
                    interest_reason = "AI/ML interests align with AI Engineer roles."
                
            if norm_user_domain == norm_db_domain:
                domain_score = 100.0
            else:
                domain_score = 0.0
                
            # Step 5: Final Calculation
            raw_score = (0.5 * skill_score) + (0.2 * cgpa_score) + (0.15 * interest_score) + (0.15 * domain_score)
            final_score = round(raw_score)
            
            print(f"Debug -> skill_score: {skill_score:.2f}, cgpa_score: {cgpa_score:.2f}, interest_score: {interest_score:.2f}, domain_score: {domain_score:.2f}, raw: {raw_score:.2f}, final_score: {final_score}")
            
            # Status Mapping
            if final_score > 85:
                status = "Optimal Match"
            elif final_score >= 50:
                status = "Good Fit"
            else:
                status = "Low Compatibility"
            
            # 4. Extract Missing Skills
            missing_skills = [s for s in db_skills if s not in user_skills]

            results.append({
                "role": row["role"],
                "domain": row['domain'],
                "missing_skills": missing_skills,
                "compatibility_score": final_score,
                "status": status,
                "interest_score": interest_score,
                "interest_status": interest_status,
                "interest_reason": interest_reason
            })
            
        # Sorting
        results.sort(key=lambda x: x["compatibility_score"], reverse=True)

        if not results:
            return jsonify({})

        top_match = results[0]
        
        # Recommendations Generator
        def get_recommendation(skill_name):
            s = skill_name.lower()
            if any(k in s for k in ['sql', 'database', 'excel']): return f"SQL & Data Basics Course"
            if 'python' in s: return f"Python Mini-Project"
            if any(k in s for k in ['react', 'html', 'css', 'javascript']): return f"Frontend Web Project"
            if 'java' in s: return f"Java Application Project"
            if 'aws' in s or 'cloud' in s or 'azure' in s: return f"Cloud Deployment Lab"
            if 'linux' in s or 'bash' in s: return f"Linux & Scripting Tutorial"
            if 'machine learning' in s or 'ai' in s or 'tensorflow' in s or 'pytorch' in s: return f"Machine Learning Model Project"
            if 'docker' in s or 'kubernetes' in s: return f"Containerization Basics"
            return f"Brush up on {skill_name} fundamentals"
            
        recommendations = [get_recommendation(s) for s in top_match["missing_skills"]]
        
        # Top 3 Matches
        top_matches = [{"role": r["role"], "score": r["compatibility_score"], "missing_skills": r["missing_skills"]} for r in results[:3]]
        
        response_payload = {
            "role": top_match["role"],
            "score": top_match["compatibility_score"],
            "missing_skills": top_match["missing_skills"],
            "recommendations": recommendations,
            "top_matches": top_matches,
            "interest_score": top_match["interest_score"],
            "interest_status": top_match["interest_status"],
            "interest_reason": top_match["interest_reason"]
        }
        
        return jsonify(response_payload)
        
    except sqlite3.Error as e:
        return jsonify({"error": f"Database Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
