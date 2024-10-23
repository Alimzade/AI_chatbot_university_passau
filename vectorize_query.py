import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

def vectorize_and_store_courses(courses, file_name, faculty_list):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df = pd.DataFrame(courses)
    df.drop_duplicates(subset=['Course Code', 'PN Number'], inplace=True)
    
    df['Faculty'] = faculty_list

    df['combined'] = df[['Course Title', 'Dozent(in)/Lecturer', 'Sprache/Language of instruction', 'Zuordnung zum Curriculum/Curriculum',
                         'ECTS/Credits', 'Empfohlene Vorkenntnisse/Recommended skills', 'Angestrebte Lernergebnisse/Learning outcomes', 'Inhalt/Course content', 'Studien-/Prüfungsleistungen/Assessment']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

    embeddings = model.encode(df['combined'].tolist(), convert_to_tensor=True)
    
    with open(file_name, 'wb') as f:
        pickle.dump((embeddings, df), f)

def query_modules(query, similarity_threshold=0.45):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    with open('module_embeddings/ai_course_embeddings.pkl', 'rb') as f:
        ai_embeddings, ai_df = pickle.load(f)

    with open('module_embeddings/cs_course_embeddings.pkl', 'rb') as f:
        cs_embeddings, cs_df = pickle.load(f)

    all_df = pd.concat([ai_df, cs_df], ignore_index=True).drop_duplicates(subset=['Course Code', 'PN Number'])
    
    ai_valid_indices = ai_df.drop_duplicates(subset=['Course Code', 'PN Number']).index
    cs_valid_indices = cs_df.drop_duplicates(subset=['Course Code', 'PN Number']).index

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    all_embeddings = torch.cat([ai_embeddings[ai_valid_indices], cs_embeddings[cs_valid_indices]], dim=0).to(device)

    query_embedding = model.encode(query, convert_to_tensor=True).to(device)
    
    # Calculating cosine similarities between the query and all embeddings
    similarities = util.pytorch_cos_sim(query_embedding, all_embeddings).cpu().numpy().flatten()

    threshold_indices = [i for i, similarity in enumerate(similarities) if similarity >= similarity_threshold]

    # Ensure that indices are within bounds of all_df
    valid_indices = [i for i in threshold_indices if i < len(all_df)]
    
    if valid_indices:
        filtered_df = all_df.iloc[valid_indices].copy()
        filtered_similarities = similarities[valid_indices]
        filtered_df.loc[:, 'similarity'] = filtered_similarities
        filtered_df = filtered_df.sort_values(by='similarity', ascending=False).reset_index(drop=True)
    else:
        filtered_df = pd.DataFrame()  # Always return a DataFrame, even if empty

    return filtered_df
