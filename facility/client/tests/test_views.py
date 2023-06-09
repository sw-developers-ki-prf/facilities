from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from client.models import Contact, Category, Device, Faculty, Department, Laboratory, Usage
from django.shortcuts import get_object_or_404

class AboutPageTests(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(AboutPageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get("about")
        self.assertEqual(response, 200)
    """
    def test_url_available_by_name(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")

    def test_template_content(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "<h2>About</h2>")
        self.assertNotContains(response, "Under construction ...")


class HelpPageTests(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(HelpPageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 200)
    """
    def test_url_available_by_name(self):
        response = self.client.get(reverse("help"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("help"))
        self.assertTemplateUsed(response, "help.html")

    def test_template_content(self):
        response = self.client.get(reverse("help"))
        self.assertContains(response, "<h2>Help</h2>")
        self.assertNotContains(response, "Under construction ...")


class HomePageTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(HomePageTests, self).__init__(*args, **kwargs)

    """
    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
    """
    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        #self.assertContains(response, "<h2>Facilities</h2>")
        self.assertNotContains(response, "Under construction ...")

class ContactsPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Contact.objects.create(name='Test Contact 1')
        Contact.objects.create(name='Test Contact 2')

    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertTemplateUsed(response, "contacts.html")

    def test_view_displays_contacts(self):
        response = self.client.get(reverse("contacts", args=("name",)))
        self.assertContains(response, 'Test Contact 1')
        self.assertContains(response, 'Test Contact 2')

class FacultyDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up two Faculties, Categories, Departments, Laboratories, and Devices
        cls.faculty1 = Faculty.objects.create(name='Faculty 1')
        cls.category1 = Category.objects.create(name='Category 1')
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty1)
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', faculty=cls.faculty1)
        cls.device1 = Device.objects.create(name='Device 1', category=cls.category1,
                                            department=cls.department1, laboratory=cls.laboratory1,
                                            faculty=cls.faculty1)

        cls.faculty2 = Faculty.objects.create(name='Faculty 2')
        cls.category2 = Category.objects.create(name='Category 2')
        cls.department2 = Department.objects.create(name='Department 2', faculty=cls.faculty2)
        cls.laboratory2 = Laboratory.objects.create(name='Laboratory 2', faculty=cls.faculty2)
        cls.device2 = Device.objects.create(name='Device 2', category=cls.category2,
                                            department=cls.department2, laboratory=cls.laboratory2,
                                            faculty=cls.faculty2)

    def test_response_data(self):
        response = self.client.get(reverse('facultydevices', args=[self.faculty1.id]))

        # Convert response content to string
        content = str(response.content)

        # Check the devices of faculty1 are in the response content
        self.assertIn(self.device1.name, content)
        self.assertIn(self.category1.name, content)
        self.assertIn(self.department1.name, content)
        self.assertIn(self.laboratory1.name, content)

        # Check the devices of faculty2 are not in the response content
        self.assertNotIn(self.device2.name, content)
        self.assertNotIn(self.category2.name, content)
        self.assertNotIn(self.department2.name, content)
        self.assertNotIn(self.laboratory2.name, content)

class CategoryDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Categories and two Devices for each category
        cls.category1 = Category.objects.create(name='Category 1')
        cls.device1a = Device.objects.create(name='Device 1a', category=cls.category1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', category=cls.category1, faculty=cls.faculty)

        cls.category2 = Category.objects.create(name='Category 2')
        cls.device2a = Device.objects.create(name='Device 2a', category=cls.category2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', category=cls.category2, faculty=cls.faculty)

    def test_response_data(self):
        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of category1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of category2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('categorydevices', kwargs={'category_id': self.category1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class DepartmentDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Departments and two Devices for each department
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty)
        cls.device1a = Device.objects.create(name='Device 1a', department=cls.department1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', department=cls.department1, faculty=cls.faculty)

        cls.department2 = Department.objects.create(name='Department 2', faculty=cls.faculty)
        cls.device2a = Device.objects.create(name='Device 2a', department=cls.department2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', department=cls.department2, faculty=cls.faculty)

    def test_response_data(self):
        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of department1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of department2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('departmentdevices', kwargs={'department_id': self.department1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class LaboratoryDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Laboratories and two Devices for each laboratory
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', faculty=cls.faculty)
        cls.device1a = Device.objects.create(name='Device 1a', laboratory=cls.laboratory1, faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', laboratory=cls.laboratory1, faculty=cls.faculty)

        cls.laboratory2 = Laboratory.objects.create(name='Laboratory 2', faculty=cls.faculty)
        cls.device2a = Device.objects.create(name='Device 2a', laboratory=cls.laboratory2, faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', laboratory=cls.laboratory2, faculty=cls.faculty)

    def test_response_data(self):
        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of laboratory1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of laboratory2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('laboratorydevices', kwargs={'laboratory_id': self.laboratory1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

from django.urls import reverse

class UsageDevicesListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty = Faculty.objects.create(name='Test Faculty')

        # Set up two Usages and two Devices for each usage
        cls.usage1 = Usage.objects.create(academical_usage='Usage 1')
        cls.device1a = Device.objects.create(name='Device 1a', faculty=cls.faculty)
        cls.device1b = Device.objects.create(name='Device 1b', faculty=cls.faculty)
        cls.device1a.usages.add(cls.usage1)
        cls.device1b.usages.add(cls.usage1)

        cls.usage2 = Usage.objects.create(academical_usage='Usage 2')
        cls.device2a = Device.objects.create(name='Device 2a', faculty=cls.faculty)
        cls.device2b = Device.objects.create(name='Device 2b', faculty=cls.faculty)
        cls.device2a.usages.add(cls.usage2)
        cls.device2b.usages.add(cls.usage2)

    def test_response_data(self):
        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        content = str(response.content)

        # Check the devices of usage1 are in the response content
        self.assertIn(self.device1a.name, content)
        self.assertIn(self.device1b.name, content)

        # Check the devices of usage2 are not in the response content
        self.assertNotIn(self.device2a.name, content)
        self.assertNotIn(self.device2b.name, content)

    def test_ordering(self):
        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'desc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1b, self.device1a])

        response = self.client.get(reverse('usagedevices', kwargs={'usage_id': self.usage1.id, 'order': 'asc'}))
        devices = list(response.context['devices'])
        self.assertEqual(devices, [self.device1a, self.device1b])

class SearchResultViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up Faculty for the devices
        cls.faculty1 = Faculty.objects.create(name='Test Faculty 1')

        # Set up Category for the devices
        cls.category1 = Category.objects.create(name='Category 1')

        # Set up Department for the devices
        cls.department1 = Department.objects.create(name='Department 1', faculty=cls.faculty1)

        # Set up Laboratory for the devices
        cls.laboratory1 = Laboratory.objects.create(name='Laboratory 1', adress='Address 1', faculty=cls.faculty1)

        # Set up Usage for the devices
        cls.usage1 = Usage.objects.create(academical_usage='Usage 1')

        # Set up Contact for the devices
        cls.contact1 = Contact.objects.create(name='Contact 1', email='contact1@test.com', phone='123456789')

        # Set up Device
        cls.device1 = Device.objects.create(
            name='Device 1',
            serial_number='1234',
            faculty=cls.faculty1,
            contact=cls.contact1,
            laboratory=cls.laboratory1,
            department=cls.department1,
            category=cls.category1,
        )
        cls.device1.usages.add(cls.usage1)

    def test_search_by_device_name(self):
        response = self.client.get(reverse('search_result') + '?query=Device%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_serial_number(self):
        response = self.client.get(reverse('search_result') + '?query=1234')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_name(self):
        response = self.client.get(reverse('search_result') + '?query=Contact%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_email(self):
        response = self.client.get(reverse('search_result') + '?query=contact1@test.com')
        self.assertContains(response, 'Device 1')

    def test_search_by_contact_phone(self):
        response = self.client.get(reverse('search_result') + '?query=123456789')
        self.assertContains(response, 'Device 1')

    def test_search_by_academical_usage(self):
        response = self.client.get(reverse('search_result') + '?query=Usage%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_laboratory_name(self):
        response = self.client.get(reverse('search_result') + '?query=Laboratory%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_laboratory_address(self):
        response = self.client.get(reverse('search_result') + '?query=Address%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_faculty_name(self):
        response = self.client.get(reverse('search_result') + '?query=Test%20Faculty%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_department_name(self):
        response = self.client.get(reverse('search_result') + '?query=Department%201')
        self.assertContains(response, 'Device 1')

    def test_search_by_category_name(self):
        response = self.client.get(reverse('search_result') + '?query=Category%201')
        self.assertContains(response, 'Device 1')
