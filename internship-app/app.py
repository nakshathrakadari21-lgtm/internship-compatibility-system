from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection
@app.route("/")
def home():
    return render_template("index.html")

def normalize_string(s):
    if not s:
        return ""
    # Convert to lowercase and remove spaces and special characters
    s = s.lower().replace(" ", "").replace("/", "")
    if s in ["webdevelopment", "webdev"]:
        return "webdev"
    elif s in ["datascience"]:
        return "datascience"
    elif s in ["aiml", "ai", "machinelearning"]:
        return "aiml"
    return s

def get_db_connection():
    conn = sqlite3.connect('internships.db')
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

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
                
            # Step 2: Skill Matching (60% Weight)
            db_skills_raw = row['skills'].split(',')
            db_skills = set([s.strip().lower() for s in db_skills_raw if s.strip()])
            
            if len(db_skills) == 0:
                skill_score = 0.0
            else:
                matching_skills = user_skills.intersection(db_skills)
                skill_score = (len(matching_skills) / len(db_skills)) * 100
                
            # Step 3: Domain/Interest Bonus (40% Weight)
            req_domain_lower = row['domain'].lower()
            role_title_lower = row['role'].lower()
            
            domain_bonus_points = 0
            norm_user_interest = normalize_string(user_interest)
            norm_user_domain = normalize_string(user_domain)
            norm_db_domain = normalize_string(row['domain'])
            
            domain_matched = norm_user_domain == norm_db_domain or (norm_user_interest and norm_user_interest == norm_db_domain)
            
            if domain_matched:
                domain_bonus_points += 20
                
            if user_interest and user_interest in role_title_lower:
                domain_bonus_points += 10
                
            # Step 4: Final Calculation
            if skill_score >= 99.99 and domain_matched:
                final_score = 100.0
            else:
                final_score = (0.6 * skill_score) + (0.4 * domain_bonus_points)
            
            # Status Mapping
            if final_score > 85:
                status = "Optimal Match"
            elif final_score >= 50:
                status = "Good Fit"
            else:
                status = "Low Compatibility"
            
            # 4. Response Format
            results.append({
                "role": row["role"],
                "domain": row['domain'],
                "required_skills": list(db_skills),
                "compatibility_score": round(final_score, 2),
                "status": status
            })
            
        # Sorting
        results.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return jsonify(results)
        
    except sqlite3.Error as e:
        return jsonify({"error": f"Database Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
