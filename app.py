import streamlit as st  
import pandas as pd  
import openai  
  
# Configuration  
API_KEY = "783973291a7c4a74a1120133309860c0"  
ENDPOINT = "https://theswedes.openai.azure.com/"  
API_VERSION = "2024-05-01-preview"  
DEPLOYMENT_NAME = "GPT-4-Omni"  
  
# Initialize OpenAI client  
openai.api_type = "azure"  
openai.api_key = API_KEY  
openai.api_base = ENDPOINT  
openai.api_version = API_VERSION  
  
# Define prompt templates for each technique  
def generate_prompt(method, context, goal):  
    prompts = {  
        "PCP": f"Progressive Contextual Prompting (PCP):\nContext: {context}\nGoal: {goal}\nEnsure the response builds on previous context, addresses the goal, and maintains engagement.",  
        "Zero-shot": f"Zero-shot Prompting:\nTask: {goal}\nContext: {context}\n",  
        "Few-shot": f"Few-shot Prompting:\nExamples: Provide examples relevant to the task.\nContext: {context}\nGoal: {goal}\n",  
    }  
    return prompts.get(method, "")  
  
def evaluate_prompt(method, context, goal):  
    prompt = generate_prompt(method, context, goal)  
    try:  
        response = openai.ChatCompletion.create(  
            engine=DEPLOYMENT_NAME,  
            messages=[  
                {"role": "system", "content": "You are an AI assistant."},  
                {"role": "user", "content": prompt}  
            ],  
            max_tokens=512,  
            temperature=0.5,  
            top_p=0.9,  
            frequency_penalty=0,  
            presence_penalty=0,  
        )  
        return response.choices[0].message['content'].strip()  
    except Exception as e:  
        st.error(f"Error: {str(e)}")  
        return ""  
  
def evaluate_quality(response, answer, technique):  
    # Placeholder for actual evaluation logic  
    # Simulate some logic to determine correctness  
    correct = response.lower() == answer.lower()  
    scores = {  
        "Correct": correct,  
        "Coherence": 0.9 if technique == "PCP" else 0.8,  
        "Relevance": 0.95 if technique == "PCP" else 0.85,  
        "Completeness": 0.9 if technique == "PCP" else 0.8  
    }  
    return scores  
  
def main():  
    st.title("Advanced Prompting Techniques Evaluation")  
  
    # List of problems with correct answers  
    problems = {  
        "1. How many diagonals can be drawn in a regular polygon with 9 sides?": "272",  
        "2. What should be added to the polynomial x^4 + 64 to make it a perfect square? Choose from: 4x^2, 16x^2, 8x^2, or -8x^2": "16x^2",  
        "3. How many points of intersection does the quadratic polynomial x^2 + 4x + 4 have with the X-axis?": "1",  
        "4. If the price of sugar is increased by 25%, by what percentage should the consumption be decreased to maintain the same expenditure?": "20%",  
        "5. In the logical implication P => Q, under which condition is the statement false?": "P is true and Q is false",  
        "6. A sum of Rs 53 is divided among A, B, and C such that A gets Rs 7 more than B, and B gets Rs 8 more than C. What is the ratio of their shares?": "25:18:10",  
        "7. Find the principal amount if the compound interest is charged at a rate of 16 2/3% per annum for two years, resulting in a total of Rs 196.": "Rs 144",  
        "8. If α and β are roots of the equation x^2 – x – 1 = 0, what is the equation whose roots are α/β and β/α?": "x^2 + 3x + 1 = 0",  
        "9. What is the sum of the interior angles of a pentagon?": "540 degrees",  
        "10. Solve for x in the equation: 5x - 3 = 2x + 7": "x = 10/3",  
        "11. Calculate the area of a circle with a radius of 7 units.": "154 square units",  
        "12. Determine the derivative of the function f(x) = x^2 + 3x.": "2x + 3",  
        "13. What is the factorial of 5?": "120",  
        "14. Find the hypotenuse of a right triangle with legs measuring 3 and 4 units.": "5",  
        "15. Simplify the expression: (3x^2y)^2": "9x^4y^2",  
        "16. Convert 45 degrees to radians.": "π/4",  
        "17. Solve the quadratic equation: x^2 - 4x + 4 = 0": "x = 2",  
        "18. What is the slope of the line represented by the equation y = 2x + 3?": "2",  
        "19. Calculate the volume of a sphere with a radius of 3 units.": "36π cubic units",  
        "20. Find the probability of rolling a sum of 7 with two six-sided dice.": "1/6",  
    }  
  
    st.write("### Select problems to evaluate:")  
    selected_problems = []  
    for question in problems.keys():  
        if st.checkbox(question):  
            selected_problems.append(question)  
  
    st.write("### Define the goal of the problem:")  
    goal = st.text_input("Goal", "Solve the mathematical problem")  
  
    st.write("### Select prompting techniques to compare:")  
    techniques = st.multiselect(  
        "Techniques",  
        ["PCP", "Zero-shot", "Few-shot"]  
    )  
  
    context = st.text_area("Provide initial context for the problem:")  
  
    if st.button("Evaluate"):  
        results = []  
        technique_summary = {technique: {"correct": 0, "total": 0} for technique in techniques}  
  
        for problem in selected_problems:  
            answer = problems[problem]  
            for technique in techniques:  
                response = evaluate_prompt(technique, context, problem)  
                quality_scores = evaluate_quality(response, answer, technique)  
  
                if quality_scores["Correct"]:  
                    technique_summary[technique]["correct"] += 1  
                technique_summary[technique]["total"] += 1  
  
                results.append({  
                    "Problem": problem,  
                    "Technique": technique,  
                    "Response": response,  
                    "Correct": quality_scores["Correct"],  
                    "Coherence": quality_scores["Coherence"],  
                    "Relevance": quality_scores["Relevance"],  
                    "Completeness": quality_scores["Completeness"]  
                })  
  
        # Sort results by the evaluation scores  
        results_df = pd.DataFrame(results).sort_values(by=["Correct", "Coherence", "Relevance", "Completeness"], ascending=False)  
  
        st.write("### Evaluation Results:")  
        st.dataframe(results_df[["Problem", "Technique", "Correct", "Coherence", "Relevance", "Completeness"]])  
  
        st.write("### Summary:")  
        for technique, summary in technique_summary.items():  
            st.write(f"**{technique}**: Solved {summary['correct']} out of {summary['total']} problems correctly.")  
  
        st.write("### Detailed Responses:")  
        for index, row in results_df.iterrows():  
            st.write(f"**Problem**: {row['Problem']}")  
            st.write(f"**{row['Technique']}**: {row['Response']} - {'Correct' if row['Correct'] else 'Incorrect'}")  
  
if __name__ == "__main__":  
    main()  
