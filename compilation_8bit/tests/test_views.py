from django.urls import reverse

import compilation_8bit.views as views

# from django.urls import reverse

from django.test import TestCase
from django.contrib.auth.models import User

from compilation_8bit.models import File, Directory


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user.save()

    def setUp(self):
        pass

    def test_basic(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        response = self.client.get(reverse("compilation_8bit:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compilation_8bit/index.html")


class DeleteObjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='bbsdfafd1&1b')
        test_user2.save()

        cls.test_user1 = test_user1
        cls.test_user2 = test_user2

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
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        request = reverse("compilation_8bit:del_file") + "?id=" + str(self.file_1_usr1.id)
        response = self.client.get(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.get(pk=self.file_1_usr1.id).is_deleted)

    def testDelDir(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')

        response = self.client.get(reverse("compilation_8bit:del_dir") + "?id=" + str(self.dir_1_usr1.id))

        self.assertEqual(response.status_code, 200)

        # now directory and its both files should be marked as deleted
        self.assertTrue(File.objects.get(pk=self.file_1_usr1.id).is_deleted)
        self.assertTrue(File.objects.get(pk=self.file_2_usr1.id).is_deleted)
        self.assertTrue(Directory.objects.get(pk=self.dir_1_usr1.id).is_deleted)


    def testDelFileOfOtherUser(self):
        self.client.login(username='testuser2', password='bbsdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=" + str(self.file_1_usr1.id))

        self.assertEqual(response.status_code, 400)

        self.assertFalse(self.file_1_usr1.is_deleted)

    def testDelDirOfOtherUser(self):
        self.client.login(username='testuser2', password='bbsdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_dir") + "?id=" + str(self.dir_1_usr1.id))

        self.assertEqual(response.status_code, 400)

        self.assertFalse(self.dir_1_usr1.is_deleted)

    def testDelNotExistingFile(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=sadfjsfla")

        self.assertEqual(response.status_code, 400)

    def testDelNotExistingDir(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        response = self.client.get(reverse("compilation_8bit:del_file") + "?id=sadfjsfla")

        self.assertEqual(response.status_code, 400)


class AddDirTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='bbsdfafd1&1b')
        test_user2.save()

        cls.test_user1 = test_user1
        cls.test_user2 = test_user2

    def setUp(self):
        dir_1_usr1 = Directory.objects.create(name="dir_1", owner=self.test_user1)
        dir_1_usr1.save()

        self.dir_1_usr1 = dir_1_usr1

    def testBasicAdd(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"parent_id": str(self.dir_1_usr1.id), "dir_name": "new_dir"}
        response = self.client.post(reverse("compilation_8bit:add_dir"), data)

        self.assertEqual(response.status_code, 200)

        new_dir = Directory.objects.get(name="new_dir")

        self.assertEqual(new_dir.parent, self.dir_1_usr1)

    def testRootAdd(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"dir_name": "new_dir"}
        response = self.client.post(reverse("compilation_8bit:add_dir"), data)

        self.assertEqual(response.status_code, 200)
        new_dir = Directory.objects.get(name="new_dir")
        self.assertEqual(new_dir.parent, None)

    def testBadName(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"dir_name": "toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo long name"}
        response = self.client.post(reverse("compilation_8bit:add_dir"), data)
        self.assertEqual(response.status_code, 400)

    def testBadUser(self):
        self.client.login(username='testuser2', password='bbsdfafd1&1b')
        data = {"parent_id": str(self.dir_1_usr1.id), "dir_name": "new_dir"}
        response = self.client.post(reverse("compilation_8bit:add_dir"), data)

        self.assertEqual(response.status_code, 400)
class AddFileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='aasdfafd1&1b')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='bbsdfafd1&1b')
        test_user2.save()

        cls.test_user1 = test_user1
        cls.test_user2 = test_user2

    def setUp(self):
        dir_1_usr1 = Directory.objects.create(name="dir_1", owner=self.test_user1)
        dir_1_usr1.save()

        self.dir_1_usr1 = dir_1_usr1


    def testBasicAdd(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"parent_id": str(self.dir_1_usr1.id), "file_name": "new_file", "content": "new_content"}
        response = self.client.post(reverse("compilation_8bit:add_file"), data)

        self.assertEqual(response.status_code, 200)

        new_file = File.objects.get(name="new_file")

        self.assertEqual(new_file.content, "new_content")
        self.assertEqual(new_file.parent, self.dir_1_usr1)

    def testBadParent(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"parent_id": "aaaa", "file_name": "new_file", "content": "new_content"}
        response = self.client.post(reverse("compilation_8bit:add_file"), data)

        self.assertEqual(response.status_code, 400)

    def testNoContent(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"parent_id": self.dir_1_usr1, "file_name": "new_file"}
        response = self.client.post(reverse("compilation_8bit:add_file"), data)

        self.assertEqual(response.status_code, 400)

    def testNoName(self):
        self.client.login(username='testuser1', password='aasdfafd1&1b')
        data = {"parent_id": self.dir_1_usr1, "content": "new_content"}
        response = self.client.post(reverse("compilation_8bit:add_file"), data)

        self.assertEqual(response.status_code, 400)

