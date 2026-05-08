[33mcommit 5b180ff6c5b1509036276522f8ff8f1d204bca8b[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mdiyprojects[m[33m)[m
Author: jdtcalanno <joshua.dame.calanno@student.ateneo.edu>
Date:   Thu May 7 12:02:36 2026 +0800

    Implemented new models

[1mdiff --git a/diyprojects/models.py b/diyprojects/models.py[m
[1mindex ce92702..bfd8f85 100644[m
[1m--- a/diyprojects/models.py[m
[1m+++ b/diyprojects/models.py[m
[36m@@ -1,4 +1,5 @@[m
 from django.db import models[m
[32m+[m[32mfrom django.core.validators import MaxValueValidator, MinValueValidator[m[41m [m
 [m
 [m
 class ProjectCategory(models.Model):[m
[36m@@ -33,3 +34,36 @@[m [mclass Project(models.Model):[m
 [m
     def __str__(self) -> str:[m
         return self.title[m
[32m+[m[41m    [m
[32m+[m[32mclass Favorite(models.Model):[m
[32m+[m[32m    project = models.ForeignKey([m
[32m+[m[32m        "Project",[m
[32m+[m[32m        on_delete=models.CASCADE,[m
[32m+[m[32m    )[m
[32m+[m[32m    profile = models.ForeignKey([m
[32m+[m[32m        "Profile",[m
[32m+[m[32m        on_delete=models.CASCADE,[m
[32m+[m[32m    )[m
[32m+[m[32m    date_favorited = models.DateTimeField(auto_now_add=True)[m
[32m+[m[32m    status_choices = [[m
[32m+[m[32m        ('Backlog', 'Backlog'),[m
[32m+[m[32m        ('To-Do', 'To-Do'),[m
[32m+[m[32m        ('Done', 'Done'),[m
[32m+[m[32m    ][m
[32m+[m[32m    project_status = models.CharField(choices=status_choices,default='Backlog')[m
[32m+[m
[32m+[m[32mclass ProjectReview(models.Model):[m
[32m+[m[32m    reviewer = models.ForeignKey([m
[32m+[m[32m        "Profile",[m
[32m+[m[32m        on_delete=models.CASCADE,[m
[32m+[m[32m    )[m
[32m+[m[32m    comment = models.TextField()[m
[32m+[m[32m    image = models.ImageField()[m
[32m+[m
[32m+[m[32mclass ProjectRating(models.Model):[m
[32m+[m[32m    profile = models.ForeignKey([m
[32m+[m[32m        "Profile",[m
[32m+[m[32m        on_delete=models.CASCADE[m
[32m+[m[32m    )[m
[32m+[m[32m    score = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])[m
[41m+[m
