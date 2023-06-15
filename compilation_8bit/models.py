import logging

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

logging.basicConfig(filename="logfile.txt", level=logging.DEBUG)



class FilesystemItem(models.Model):
    MAX_FILE_SYSTEM_ITEM_NAME_LEN = 30

    name = models.CharField(max_length=MAX_FILE_SYSTEM_ITEM_NAME_LEN)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True)
    delete_status_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name





class Directory(FilesystemItem):
    parent = models.ForeignKey("Directory", null=True, blank=True, on_delete=models.CASCADE)

    def soft_delete(self):

        if self.is_deleted:
            return

        for d in Directory.objects.all():
            if d.parent == self:
                d.soft_delete()

        for f in File.objects.all():

            # logging.debug(f"dir id = {self.id} , file parent id = {f.parent.id} ")
            if f.parent.id == self.id:
                f.soft_delete()

        self.is_deleted = True
        self.delete_status_date = timezone.now()

        self.save()


class File(FilesystemItem):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    def soft_delete(self):

        if self.is_deleted:
            return

        self.is_deleted = True
        self.delete_status_date = timezone.now()

        self.save()


# class SectionType(models.Model):
#
#     PROCEDURE = 0
#     COMMENT = 1
#     DIRECTIVE = 2
#     VARS_DECLARATION = 3
#     ASSEMBLY_CODE = 4
#
#     TYPE = (
#         (PROCEDURE, "procedure"),
#         (COMMENT, "comment"),
#         (DIRECTIVE, "directive"),
#         (VARS_DECLARATION, "variables declaration"),
#         (ASSEMBLY_CODE, "assembly code")
#     )
#
#     type = models.PositiveSmallIntegerField(choices=TYPE)
#
#
# class SectionStatus(models.Model):
#
#     COMPILATION_OK = 0
#     COMPILATION_WARNING = 1
#     COMPILATION_ERROR = 2
#     UNKNOWN = 3
#
#     STATUS = (
#         (COMPILATION_OK, "compiles without warnings"),
#         (COMPILATION_WARNING, "compiles with warning(s)"),
#         (COMPILATION_ERROR, "not compiles"),
#         (UNKNOWN, "not compiled yet")
#     )
#
#     status = models.PositiveSmallIntegerField(choices=STATUS)
#
#
# class CompilationStatusInfo(models.Model):
#
#     section_status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
#
#     code_line = models.PositiveIntegerField()
#
#     info = models.TextField()
#
#     WARNING = 0
#     ERROR = 1
#
#     TYPE = (
#         (WARNING, "warning"),
#         (ERROR, "error"),
#     )
#
#     info_type = models.PositiveSmallIntegerField(choices=TYPE)
#
#
# class Section(models.Model):
#
#     name = models.CharField(max_length=30)
#     description = models.TextField(null=True, blank=True)
#
#     start = models.PositiveIntegerField()
#     end = models.PositiveIntegerField()
#
#     status = models.OneToOneField(SectionStatus, on_delete=models.PROTECT)


def restore_all():

    for f in File.objects.all():
        f.is_deleted = False
        f.save()

    for d in Directory.objects.all():
        d.is_deleted = False
        d.save()




