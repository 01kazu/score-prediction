import pandas as pd
import pickle

# Its input is a list of all students registered under the course with their G1 scores
def preprocessing_g1(g1_objs):
    
    student_dict = {'matric_number': [], 'age':[], 'traveltime':[], 'studytime':[], 'failures':[], 'famrel':[], 'freetime':[],
        'goout':[], 'Dalc':[], 'Walc':[], 'health':[], 'absences':[], 'G1':[], 'school_GP':[],
        'school_MS':[], 'sex_F':[], 'sex_M':[], 'address_R':[], 'address_U':[], 'famsize_GT3':[],
        'famsize_LE3':[], 'Pstatus_A':[], 'Pstatus_T':[], 'Medu_5th to 9th grade':[],
        'Medu_higher education':[], 'Medu_none':[], 'Medu_primary edu(4th grade)':[],
        'Medu_secondary edu':[], 'Fedu_5th to 9th grade':[], 'Fedu_higher education':[],
        'Fedu_none':[], 'Fedu_primary edu(4th grade)':[], 'Fedu_secondary edu':[],
        'Mjob_at_home':[], 'Mjob_health':[], 'Mjob_other':[], 'Mjob_services':[],
        'Mjob_teacher':[], 'Fjob_at_home':[], 'Fjob_health':[], 'Fjob_other':[],
        'Fjob_services':[], 'Fjob_teacher':[], 'reason_course':[], 'reason_home':[],
        'reason_other':[], 'reason_reputation':[], 'guardian_father':[],
        'guardian_mother':[], 'guardian_other':[], 'schoolsup_no':[], 'schoolsup_yes':[],
        'famsup_no':[], 'famsup_yes':[], 'paid_no':[], 'paid_yes':[], 'activities_no':[],
        'activities_yes':[], 'nursery_no':[], 'nursery_yes':[], 'higher_no':[],
        'higher_yes':[], 'internet_no':[], 'internet_yes':[], 'romantic_no':[],'romantic_yes':[]
        }

    for g1_obj in g1_objs:

        student_dict['matric_number'].append(g1_obj.student.matric_number)

        # Gender of the student
        student_dict['age'].append(g1_obj.student.age)
        
        # Gender of the studetn
        if g1_obj.student.gender == 'male':
            student_dict['sex_M'].append(1)
        else:
            student_dict['sex_F'].append(1)
        
        # Address of the Student
        if g1_obj.student.address == 'urban':
            student_dict['address_U'].append(1)
        else:
            student_dict['address_R'].append(1)

        # Student's reason for attending the school
        if g1_obj.student.reason == 'close to home':
            student_dict['reason_home'].append(1)
        elif g1_obj.student.reason == 'school reputation':
            student_dict['reason_reputation'].append(1)
        elif g1_obj.student.reason == 'course preference':
            student_dict['reason_course'].append(1)
        else:
            student_dict['reason_other'].append(1)

        # Student's Mother's Job
        if g1_obj.student.mother_job == 'teacher':
            student_dict['Mjob_teacher'].append(1)
        elif g1_obj.student.mother_job == 'health':
            student_dict['Mjob_health'].append(1)
        elif g1_obj.student.mother_job == 'services':
            student_dict['Mjob_services'].append(1)
        elif g1_obj.student.mother_job == 'at_home':
            student_dict['Mjob_at_home'].append(1)
        else:
            student_dict['Mjob_other'].append(1)

        # The Student's Father's Job
        if g1_obj.student.father_job == 'teacher':
            student_dict['Fjob_teacher'].append(1)
        elif g1_obj.student.father_job == 'health':
            student_dict['Fjob_health'].append(1)
        elif g1_obj.student.father_job == 'services':
            student_dict['Fjob_services'].append(1)
        elif g1_obj.student.father_job == 'at_home':
            student_dict['Fjob_at_home'].append(1)
        else:
            student_dict['Fjob_other'].append(1)

        # The Student's Guardian
        if g1_obj.student.guardian == 'mother':
            student_dict['guardian_mother'].append(1) 
        elif g1_obj.student.guardian == 'father':
            student_dict['guardian_father'].append(1) 
        else:
            student_dict['guardian_other'].append(1) 

        # G1 Scores
        student_dict['G1'].append(g1_obj.score)
    
    for key in student_dict:
        while len(student_dict[key]) < len(g1_objs):            
            student_dict[key].append(0)

    student_df = pd.DataFrame(student_dict)
    print(student_df)
    return student_df
    
    

def preprocessing_g2(g2_objs, g1_scores):

    student_dict = {'matric_number':[], 'age':[], 'traveltime':[], 'studytime':[], 'failures':[], 'famrel':[], 'freetime':[],
       'goout':[], 'Dalc':[], 'Walc':[], 'health':[], 'absences':[], 'G1':[], 'G2':[], 'school_GP':[],
       'school_MS':[], 'sex_F':[], 'sex_M':[], 'address_R':[], 'address_U':[], 'famsize_GT3':[],
       'famsize_LE3':[], 'Pstatus_A':[], 'Pstatus_T':[], 'Medu_5th to 9th grade':[],
       'Medu_higher education':[], 'Medu_none':[], 'Medu_primary edu(4th grade)':[],
       'Medu_secondary edu':[], 'Fedu_5th to 9th grade':[], 'Fedu_higher education':[],
       'Fedu_none':[], 'Fedu_primary edu(4th grade)':[], 'Fedu_secondary edu':[],
       'Mjob_at_home':[], 'Mjob_health':[], 'Mjob_other':[], 'Mjob_services':[],
       'Mjob_teacher':[], 'Fjob_at_home':[], 'Fjob_health':[], 'Fjob_other':[],
       'Fjob_services':[], 'Fjob_teacher':[], 'reason_course':[], 'reason_home':[],
       'reason_other':[], 'reason_reputation':[], 'guardian_father':[],
       'guardian_mother':[], 'guardian_other':[], 'schoolsup_no':[], 'schoolsup_yes':[],
       'famsup_no':[], 'famsup_yes':[], 'paid_no':[], 'paid_yes':[], 'activities_no':[],
       'activities_yes':[], 'nursery_no':[], 'nursery_yes':[], 'higher_no':[],
       'higher_yes':[], 'internet_no':[], 'internet_yes':[], 'romantic_no':[],'romantic_yes':[]
       }
    for g2_obj, g1_obj in zip(g2_objs, g1_scores):

        student_dict['matric_number'].append(g2_obj.student.matric_number)

        # Gender of the student
        student_dict['age'].append(g2_obj.student.age)
        
        # Gender of the studetn
        if g2_obj.student.gender == 'male':
            student_dict['sex_M'].append(1)
        else:
            student_dict['sex_F'].append(1)
        
        # Address of the Student
        if g2_obj.student.address == 'urban':
            student_dict['address_U'].append(1)
        else:
            student_dict['address_R'].append(1)

        # Student's reason for attending the school
        if g2_obj.student.reason == 'close to home':
            student_dict['reason_home'].append(1)
        elif g2_obj.student.reason == 'school reputation':
            student_dict['reason_reputation'].append(1)
        elif g2_obj.student.reason == 'course preference':
            student_dict['reason_course'].append(1)
        else:
            student_dict['reason_other'].append(1)

        # Student's Mother's Job
        if g2_obj.student.mother_job == 'teacher':
            student_dict['Mjob_teacher'].append(1)
        elif g2_obj.student.mother_job == 'health':
            student_dict['Mjob_health'].append(1)
        elif g2_obj.student.mother_job == 'services':
            student_dict['Mjob_services'].append(1)
        elif g2_obj.student.mother_job == 'at_home':
            student_dict['Mjob_at_home'].append(1)
        else:
            student_dict['Mjob_other'].append(1)

        # The Student's Father's Job
        if g2_obj.student.father_job == 'teacher':
            student_dict['Fjob_teacher'].append(1)
        elif g2_obj.student.father_job == 'health':
            student_dict['Fjob_health'].append(1)
        elif g2_obj.student.father_job == 'services':
            student_dict['Fjob_services'].append(1)
        elif g2_obj.student.father_job == 'at_home':
            student_dict['Fjob_at_home'].append(1)
        else:
            student_dict['Fjob_other'].append(1)

        # The Student's Guardian
        if g2_obj.student.guardian == 'mother':
            student_dict['guardian_mother'].append(1) 
        elif g2_obj.student.guardian == 'father':
            student_dict['guardian_father'].append(1) 
        else:
            student_dict['guardian_other'].append(1) 

        # G1 Scores
        student_dict['G1'].append(g1_obj.score)

        # G2 Scores
        student_dict['G2'].append(g2_obj.score)

    for key in student_dict:
        while len(student_dict[key]) < len(g2_objs):            
            student_dict[key].append(0)

    student_df = pd.DataFrame(student_dict)
    print(student_df)
    return student_df

def classification_g1(df):
        try:
            classification_model_g1 = pickle.load(open('score/classification_model_g1.sav', 'rb'))
            predictions = classification_model_g1.predict(df)
            print(predictions)
            return predictions

        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def classification_g2(df):
        try:
            classification_model_g2 = pickle.load(open('score/classification_model.sav', 'rb'))
            predictions = classification_model_g2.predict(df)
            print(predictions)
            return predictions

        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
