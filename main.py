import pandas as pd
from extract_pdf import extract_text_from_pdf
from process_text import detect_course_headings, save_to_csv
from vectorize_query import vectorize_and_store_courses, query_modules

def main():
    try:
        ai_text = extract_text_from_pdf("module_catalogs/Modulkatalog_Master_Artificial_Intelligence_Engineering.pdf")
        cs_text = extract_text_from_pdf("module_catalogs/Modulkatalog-Master-Informatik.pdf")

        ai_courses = detect_course_headings(ai_text)
        cs_courses = detect_course_headings(cs_text)

        print(f"Number of AI courses detected: {len(ai_courses)}")
        print(f"Number of CS courses detected: {len(cs_courses)}")

        ai_courses_df = pd.DataFrame(ai_courses)
        cs_courses_df = pd.DataFrame(cs_courses)

        ai_courses_df['Faculty'] = "MSc AI Engineering"
        cs_courses_df['Faculty'] = "MSc Informatik/ Computer Science"

        # Combine both DataFrames to identify common courses
        all_courses_df = pd.concat([ai_courses_df, cs_courses_df], ignore_index=True)

        # Identify courses that appear in both DataFrames
        course_title_counts = all_courses_df['Course Title'].value_counts()
        both_courses_titles = course_title_counts[course_title_counts > 1].index

        all_courses_df.loc[all_courses_df['Course Title'].isin(both_courses_titles), 'Faculty'] = "MSc AI Engineering and MSc Informatik/ Computer Science"

        ai_courses_final = all_courses_df[all_courses_df['Faculty'].str.contains("MSc AI Engineering")].drop_duplicates(subset=['Course Title', 'Course Code'])
        cs_courses_final = all_courses_df[all_courses_df['Faculty'].str.contains("MSc Informatik/ Computer Science")].drop_duplicates(subset=['Course Title', 'Course Code'])

        vectorize_and_store_courses(ai_courses_final.to_dict(orient='records'), 'module_embeddings/ai_course_embeddings.pkl', "MSc AI Engineering")
        vectorize_and_store_courses(cs_courses_final.to_dict(orient='records'), 'module_embeddings/cs_course_embeddings.pkl', "MSc Informatik/ Computer Science")

        save_to_csv(ai_courses_final.to_dict(orient='records'), 'module_csvs/ai_courses.csv')
        save_to_csv(cs_courses_final.to_dict(orient='records'), 'module_csvs/cs_courses.csv')

        query = "Advanced design and analysis techniques"
        results = query_modules(query, similarity_threshold=0.5)
        print(results)

    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    main()
