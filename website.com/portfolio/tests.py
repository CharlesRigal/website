from django.test import TestCase
from .models import Skill, Projet

# Create your tests here.

class SkillsModelsTest(TestCase):
    def setUp(self):
        Skill.objects.create(name="skill 1", wording="un super skill qui permet de faire des test")
        Projet.objects.create(name="super projet", wording="un projet")
        Projet.objects.create(name="projet avec skill 1", wording="projet super 2")
    
    def test_asociate_a_skill_to_projet(self):
        projet = Projet.objects.get(name="super projet")
        skill = Skill.objects.get(name="skill 1")
        projet.skills.add(skill)
        self.assertEqual(projet.skills.all()[0].name , "skill 1")
    
    def test_recuperate_project_by_skill(self):
        skill = Skill.objects.get(name="skill 1")
        projects = Projet.objects.filter(skills=skill)
        self.assertEqual(projects.count(), 1)
        self.assertEqual(projects[0].name, "super projet")

