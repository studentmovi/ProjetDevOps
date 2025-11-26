import json
import os

class StudentDataManager:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), 'students_data.json')
        self.students = []
        self.load_data()
        
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.students = data.get('students', [])
                    print(f"Données chargées: {len(self.students)} étudiants")
            else:
                self.students = []
                print("Fichier de données non trouvé, liste vide créée")
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.students = []
            
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        try:
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {'students': self.students}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Données sauvegardées: {len(self.students)} étudiants")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def get_all_students(self):
        """Retourne tous les étudiants non supprimés"""
        return [s for s in self.students if not s.get('deleted', False)]
    
    def get_student_by_id(self, student_id):
        """Récupère un étudiant par son ID"""
        for student in self.students:
            if student.get('id') == student_id and not student.get('deleted', False):
                return student
        return None
    
    def update_student(self, student_id, updated_data):
        """Met à jour un étudiant"""
        for student in self.students:
            if student.get('id') == student_id:
                student.update(updated_data)
                return self.save_data()
        return False
    
    def delete_student(self, student_id):
        """Marque un étudiant comme supprimé"""
        for student in self.students:
            if student.get('id') == student_id:
                student['deleted'] = True
                return self.save_data()
        return False
    
    def add_student(self, student_data):
        """Ajoute un nouvel étudiant"""
        # Générer un nouvel ID
        max_id = max([s.get('id', 0) for s in self.students]) if self.students else 0
        student_data['id'] = max_id + 1
        student_data['deleted'] = False
        
        self.students.append(student_data)
        return self.save_data()
    
    def get_filter_options(self):
        """Retourne les options disponibles pour les filtres"""
        active_students = self.get_all_students()
        classes = set()
        annees = set()
        options = set()
        
        for student in active_students:
            if student.get('classe'):
                classes.add(student['classe'])
            if student.get('annee'):
                annees.add(student['annee'])
            if student.get('option'):
                options.add(student['option'])
                
        return {
            'classes': sorted(list(classes)),
            'annees': sorted(list(annees)),
            'options': sorted(list(options))
        }