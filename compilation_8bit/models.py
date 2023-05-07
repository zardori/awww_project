from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)


class FilesystemItem(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True)
    delete_status_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Directory(FilesystemItem):
    parent = models.ForeignKey("Directory", null=True, on_delete=models.CASCADE)


class File(FilesystemItem):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE)
    content = models.TextField(null=True)


class SectionType(models.Model):

    PROCEDURE = 0
    COMMENT = 1
    DIRECTIVE = 2
    VARS_DECLARATION = 3
    ASSEMBLY_CODE = 4

    TYPE = (
        (PROCEDURE, "procedure"),
        (COMMENT, "comment"),
        (DIRECTIVE, "directive"),
        (VARS_DECLARATION, "variables declaration"),
        (ASSEMBLY_CODE, "assembly code")
    )

    type = models.PositiveSmallIntegerField(choices=TYPE)


class SectionStatus(models.Model):

    COMPILATION_OK = 0
    COMPILATION_WARNING = 1
    COMPILATION_ERROR = 2
    UNKNOWN = 3

    STATUS = (
        (COMPILATION_OK, "compiles without warnings"),
        (COMPILATION_WARNING, "compiles with warning(s)"),
        (COMPILATION_ERROR, "not compiles"),
        (UNKNOWN, "not compiled yet")
    )

    status = models.PositiveSmallIntegerField(choices=STATUS)


class CompilationStatusInfo(models.Model):

    section_status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)

    code_line = models.PositiveIntegerField()

    info = models.TextField()

    WARNING = 0
    ERROR = 1

    TYPE = (
        (WARNING, "warning"),
        (ERROR, "error"),
    )

    info_type = models.PositiveSmallIntegerField(choices=TYPE)


class Section(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(null=True)

    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

    status = models.OneToOneField(SectionStatus, on_delete=models.PROTECT)






