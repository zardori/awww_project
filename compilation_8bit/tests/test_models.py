from django.test import TestCase

from compilation_8bit.models import File, Directory
from django.contrib.auth.models import User


class FilesystemModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user1.save()

        cls.test_user1 = test_user1

    def setUp(self):
        dir_1_usr1 = Directory.objects.create(name="dir_1", owner=self.test_user1)

        dir_1_usr1.save()

        file_1_usr1 = File.objects.create(name="file_1", content="file_1_content", parent=dir_1_usr1,
                                          owner=self.test_user1)

        file_2_usr1 = File.objects.create(name="file_2", content="file_2_content", parent=dir_1_usr1,
                                          owner=self.test_user1)

        file_1_usr1.save()
        file_2_usr1.save()

        self.file_1_usr1 = file_1_usr1
        self.file_2_usr1 = file_2_usr1
        self.dir_1_usr1 = dir_1_usr1

    def testDelFile(self):
        self.file_1_usr1.soft_delete()

        self.assertTrue(File.objects.get(name="file_1").is_deleted)

    def testDelDir(self):
        self.dir_1_usr1.soft_delete()

        self.assertTrue(File.objects.get(name="file_1").is_deleted)
        self.assertTrue(File.objects.get(name="file_2").is_deleted)
        self.assertTrue(Directory.objects.get(name="dir_1").is_deleted)

    def testStr(self):
        self.assertEqual(str(self.file_1_usr1), self.file_1_usr1.name)
