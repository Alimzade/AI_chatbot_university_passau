import re
import csv

def clean_text(text):
    pattern = re.compile(r'\d+Modulkatalog Module Descriptions')
    return pattern.sub('', text).strip()

def detect_course_headings(text):
    courses = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.endswith('-'):
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
                line = line[:-1] + lines[i + 1].strip()[1:]
                i += 1
            line = line.strip()
        else:
            line = line.strip()

        lines[i] = clean_text(line)
        i += 1

    i = 0
    while i < len(lines):
        match = re.match(r'^(\d{4}) (.*)', lines[i])
        if match:
            course_code = match.group(1).strip()
            course_title = match.group(2).strip()
            
            pn_number_match = re.search(r'PN (\d+)', course_title)
            pn_number = pn_number_match.group(1) if pn_number_match else 'Not found'
            course_title = re.sub(r'PN \d+', '', course_title).strip()
            
            i += 1
            
            # Extracting "Häufigkeit des Modulangebots/Frequency of course offering"
            frequency_line = ''
            while i < len(lines) and not re.match(r'^Moduldauer', lines[i]):
                line = lines[i].strip()
                if 'Häufigkeit des Modulangebots' in line:
                    frequency_line = line.split('Häufigkeit des Modulangebots', 1)[1].strip()
                elif 'Frequency of course offering' in line:
                    frequency_line += ' ' + line.split('Frequency of course offering', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        frequency_line += " " + line.strip()
                    else:
                        frequency_line += line[:-1].rstrip()
                
                i += 1

            frequency_line = re.sub(r'(\w)([A-Z])', r'\1 \2', frequency_line)
            frequency_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', frequency_line)
            frequency_line = frequency_line.strip()

            # Extracting "Moduldauer/Module duration"
            duration_line = ''
            while i < len(lines) and not re.match(r'^Modulverantwortliche\(r\)', lines[i]):
                line = lines[i].strip()
                if 'Moduldauer' in line:
                    duration_line = line.split('Moduldauer', 1)[1].strip()
                elif 'Module duration' in line:
                    duration_line += ' ' + line.split('Module duration', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        duration_line += " " + line.strip()
                    else:
                        duration_line += line[:-1].rstrip()
                
                i += 1

            duration_line = re.sub(r'(\w)([A-Z])', r'\1 \2', duration_line)
            duration_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', duration_line)
            duration_line = duration_line.strip()

            # Extracting "Modulverantwortliche(r)/Module convenor"
            convenor_line = ''
            while i < len(lines) and not re.match(r'^Dozent\(in\)', lines[i]):
                line = lines[i].strip()
                if 'Modulverantwortliche(r)' in line:
                    convenor_line = line.split('Modulverantwortliche(r)', 1)[1].strip()
                elif 'Module convenor' in line:
                    convenor_line += ' ' + line.split('Module convenor', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        convenor_line += " " + line.strip()
                    else:
                        convenor_line += line[:-1].rstrip()
                
                i += 1

            convenor_line = re.sub(r'(\w)([A-Z])', r'\1 \2', convenor_line)
            convenor_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', convenor_line)
            convenor_line = convenor_line.strip()

            # Extracting "Dozent(in)/Lecturer"
            lecturer_line = ''
            while i < len(lines) and not re.match(r'^Sprache', lines[i]):
                line = lines[i].strip()
                if 'Dozent(in)' in line:
                    lecturer_line = line.split('Dozent(in)', 1)[1].strip()
                elif 'Lecturer' in line:
                    lecturer_line += ' ' + line.split('Lecturer', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        lecturer_line += " " + line.strip()
                    else:
                        lecturer_line += line[:-1].rstrip()
                
                i += 1

            lecturer_line = re.sub(r'(\w)([A-Z])', r'\1 \2', lecturer_line)
            lecturer_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', lecturer_line)
            lecturer_line = lecturer_line.strip()

            # Extracting "Sprache/Language of instruction"
            language_line = ''
            while i < len(lines) and not re.match(r'^Zuordnung zum Curriculum', lines[i]):
                line = lines[i].strip()
                if 'Sprache' in line:
                    language_line = line.split('Sprache', 1)[1].strip()
                elif 'Language of instruction' in line:
                    language_line += ' ' + line.split('Language of instruction', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        language_line += " " + line.strip()
                    else:
                        language_line += line[:-1].rstrip()
                
                i += 1

            language_line = re.sub(r'(\w)([A-Z])', r'\1 \2', language_line)
            language_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', language_line)
            language_line = language_line.strip()
            # Extracting "Zuordnung zum Curriculum/Curriculum"
            curriculum_line = ''
            while i < len(lines) and not re.match(r'^Lehrform/SWS', lines[i]):
                line = lines[i].strip()
                if 'Zuordnung zum Curriculum' in line:
                    curriculum_line = line.split('Zuordnung zum Curriculum', 1)[1].strip()
                elif 'Curriculum' in line:
                    curriculum_line += ' ' + line.split('Curriculum', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        curriculum_line += " " + line.strip()
                    else:
                        curriculum_line += line[:-1].rstrip()
                
                i += 1

            curriculum_line = re.sub(r'(\w)([A-Z])', r'\1 \2', curriculum_line)
            curriculum_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', curriculum_line)
            curriculum_line = curriculum_line.strip()

            # Extracting "Lehrform/SWS/Contact hours"
            contact_hours_line = ''
            while i < len(lines) and not re.match(r'^Arbeitsaufwand', lines[i]):
                line = lines[i].strip()
                if 'Lehrform/SWS' in line:
                    contact_hours_line = line.split('Lehrform/SWS', 1)[1].strip()
                elif 'Contact hours' in line:
                    contact_hours_line += ' ' + line.split('Contact hours', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        contact_hours_line += " " + line.strip()
                    else:
                        contact_hours_line += line[:-1].rstrip()
                
                i += 1

            contact_hours_line = re.sub(r'(\w)([A-Z])', r'\1 \2', contact_hours_line)
            contact_hours_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', contact_hours_line)
            contact_hours_line = contact_hours_line.strip()

            # Extracting "Arbeitsaufwand/Workload"
            workload_line = ''
            while i < len(lines) and not re.match(r'^ECTS', lines[i]):
                line = lines[i].strip()
                if 'Arbeitsaufwand' in line:
                    workload_line = line.split('Arbeitsaufwand', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        workload_line += " " + line.strip()
                    else:
                        workload_line += line[:-1].rstrip()
                
                i += 1

            workload_line = re.sub(r'(\w)([A-Z])', r'\1 \2', workload_line)
            workload_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', workload_line)
            workload_line = workload_line.strip()

            # Extracting "ECTS/Credits"
            ects_line = ''
            while i < len(lines) and not re.match(r'^Voraussetzungen nach Prü-', lines[i]):
                line = lines[i].strip()
                if 'ECTS' in line:
                    ects_line = line.split('ECTS', 1)[1].strip()
                elif 'Credits' in line:
                    ects_line += ' ' + line.split('Credits', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        ects_line += " " + line.strip()
                    else:
                        ects_line += line[:-1].rstrip()
                
                i += 1

            ects_line = re.sub(r'(\w)([A-Z])', r'\1 \2', ects_line)
            ects_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', ects_line)
            ects_line = ects_line.strip()

            if ects_line:
                ects_line = f"ECTS/Credits: {ects_line}"

            # Extracting "Voraussetzungen nach Prüfungsordnung/Required prerequisites as per the study and examination regulations"
            prereq_line = ''
            while i < len(lines) and not re.match(r'^Empfohlene Vorkenntnisse', lines[i]):
                line = lines[i].strip()
                if 'Voraussetzungen nach Prü-' in line:
                    prereq_line = line.split('Voraussetzungen nach Prü-', 1)[1].strip()
                elif 'fungsordnung' in line:
                    prereq_line += ' ' + line.split('fungsordnung', 1)[1].strip()
                elif 'Required prerequisites as per' in line:
                    prereq_line += ' ' + line.split('Required prerequisites as per', 1)[1].strip()
                elif 'the study and examination' in line:
                    prereq_line += ' ' + line.split('the study and examination', 1)[1].strip()
                elif 'regulations' in line:
                    prereq_line += ' ' + line.split('regulations', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        prereq_line += " " + line.strip()
                    else:
                        prereq_line += line[:-1].rstrip()
                
                i += 1

            prereq_line = re.sub(r'(\w)([A-Z])', r'\1 \2', prereq_line)
            prereq_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', prereq_line)
            prereq_line = prereq_line.strip()

            # Extracting "Empfohlene Vorkenntnisse/Recommended skills"
            skills_line = ''
            while i < len(lines) and not re.match(r'^Verwendbarkeit in weiteren', lines[i]):
                line = lines[i].strip()
                if 'Empfohlene Vorkenntnisse' in line:
                    skills_line = line.split('Empfohlene Vorkenntnisse', 1)[1].strip()
                elif 'Recommended skills' in line:
                    skills_line += ' ' + line.split('Recommended skills', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        skills_line += " " + line.strip()
                    else:
                        skills_line += line[:-1].rstrip()
                
                i += 1

            skills_line = re.sub(r'(\w)([A-Z])', r'\1 \2', skills_line)
            skills_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', skills_line)
            skills_line = skills_line.strip()

            # Extracting "Verwendbarkeit in weiteren Studiengängen/Applicability for other courses"
            applicability_line = ''
            while i < len(lines) and not re.match(r'^Angestrebte Lernergebnisse', lines[i]):
                line = lines[i].strip()
                if 'Verwendbarkeit in weiteren Studiengängen' in line:
                    applicability_line = line.split('Verwendbarkeit in weiteren Studiengängen', 1)[1].strip()
                elif 'Applicability for other courses' in line:
                    applicability_line += ' ' + line.split('Applicability for other courses', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        applicability_line += " " + line.strip()
                    else:
                        applicability_line += line[:-1].rstrip()
                
                i += 1

            applicability_line = re.sub(r'(\w)([A-Z])', r'\1 \2', applicability_line)
            applicability_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', applicability_line)
            applicability_line = applicability_line.strip()

            # Extracting "Angestrebte Lernergebnisse/Learning outcomes"
            learning_line = ''
            while i < len(lines) and not re.match(r'^Inhalt', lines[i]):
                line = lines[i].strip()
                if 'Angestrebte Lernergebnisse' in line:
                    learning_line = line.split('Angestrebte Lernergebnisse', 1)[1].strip()
                elif 'Learning outcomes ' in line:
                    learning_line += ' ' + line.split('Learning outcomes ', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        learning_line += " " + line.strip()
                    else:
                        learning_line += line[:-1].rstrip()
                
                i += 1

            learning_line = re.sub(r'(\w)([A-Z])', r'\1 \2', learning_line)
            learning_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', learning_line)
            learning_line = learning_line.strip()

            # Extracting "Inhalt/Course content"
            content_line = ''
            while i < len(lines) and not re.match(r'^Studien-/Prüfungsleistungen', lines[i]):
                line = lines[i].strip()

                if 'Inhalt' in line:
                    content_line = line.split('Inhalt', 1)[1].strip()
                elif 'Course content' in line:
                    content_line += ' ' + line.split('Course content', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        content_line += " " + line.strip()
                    else:
                        content_line += line[:-1].rstrip()
                
                i += 1

            content_line = re.sub(r'(\w)([A-Z])', r'\1 \2', content_line)
            content_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', content_line)
            content_line = content_line.strip()

            # Extracting "Studien-/Prüfungsleistungen/Assessment"
            assessment_line = ''
            while i < len(lines):
                line = lines[i].strip()
                if re.match(r'^Medienformen', line):
                    break
                if 'Studien-/Prüfungsleistungen' in line:
                    assessment_line = line.split('Studien-/Prüfungsleistungen', 1)[1].strip()
                elif 'Assessment' in line:
                    assessment_line += ' ' + line.split('Assessment', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        assessment_line += " " + line.strip()
                    else:
                        assessment_line += line[:-1].rstrip()
                
                i += 1

            assessment_line = re.sub(r'(\w)([A-Z])', r'\1 \2', assessment_line)
            assessment_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', assessment_line)
            assessment_line = assessment_line.strip()

            # Extracting "Medienformen/Media used"
            media_line = ''
            while i < len(lines) and not re.match(r'^Literatur', lines[i]):
                line = lines[i].strip()
                if 'Medienformen' in line:
                    media_line = line.split('Medienformen', 1)[1].strip()
                elif 'Media used' in line:
                    media_line += ' ' + line.split('Media used', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        media_line += " " + line.strip()
                    else:
                        media_line += line[:-1].rstrip()
                
                i += 1

            media_line = re.sub(r'(\w)([A-Z])', r'\1 \2', media_line)
            media_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', media_line)
            media_line = media_line.strip()
            
            # Extracting "Literatur/Reading list"
            reading_line = ''
            while i < len(lines) and not re.match(r'^\d{4,5} ', lines[i]):
                line = lines[i].strip()
                if 'Literatur' in line:
                    reading_line = line.split('Literatur', 1)[1].strip()
                elif 'Reading list' in line:
                    reading_line += ' ' + line.split('Reading list', 1)[1].strip()
                else:
                    if not line.endswith('-'):
                        reading_line += " " + line.strip()
                    else:
                        reading_line += line[:-1].rstrip()
                
                i += 1

            reading_line = re.sub(r'(\w)([A-Z])', r'\1 \2', reading_line)
            reading_line = re.sub(r'([.,;!?])(\S)', r'\1 \2', reading_line)
            reading_line = reading_line.strip()

            # Add course info to the list
            courses.append({
                'Course Code': course_code,
                'Course Title': course_title.strip(),
                'PN Number': pn_number,
                'Häufigkeit des Modulangebots/Frequency of course offering': frequency_line.strip() or 'Not found',
                'Moduldauer/Module duration': duration_line.strip() or 'Not found',
                'Modulverantwortliche(r)/Module convenor': convenor_line.strip() or 'Not found',
                'Dozent(in)/Lecturer': lecturer_line.strip() or 'Not found',
                'Sprache/Language of instruction': language_line.strip() or 'Not found',
                'Zuordnung zum Curriculum/Curriculum': curriculum_line.strip() or 'Not found',
                'Lehrform/SWS/Contact hours': contact_hours_line.strip() or 'Not found',
                'Arbeitsaufwand/Workload': workload_line.strip() or 'Not found',
                'ECTS/Credits': ects_line.strip() or 'Not found',
                'Voraussetzungen nach Prüfungsordnung/Required prerequisites as per the study and examination regulations': prereq_line.strip() or 'Not found',
                'Empfohlene Vorkenntnisse/Recommended skills': skills_line.strip() or 'Not found',
                'Verwendbarkeit in weiteren Studiengängen/Applicability for other courses': applicability_line.strip() or 'Not found',
                'Angestrebte Lernergebnisse/Learning outcomes': learning_line.strip() or 'Not found',
                'Inhalt/Course content': content_line.strip() or 'Not found',
                'Studien-/Prüfungsleistungen/Assessment': assessment_line.strip() or 'Not found',
                'Medienformen/Media used': media_line.strip() or 'Not found',
                'Literatur/Reading list': reading_line.strip() or 'Not found'
            })
        else:
            i += 1
    
    return courses

def save_to_csv(courses, filename='courses.csv'):
    fieldnames = courses[0].keys() if courses else []
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(courses)
