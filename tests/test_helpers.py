import pytest
import helper
import pytest_check as check
from unittest import mock
from unittest.mock import patch


class TestHelper:

	# test adding an item to the todo list and asserting that the item has been added with status NOTSTARTED
	def test_add_to_list_ok(self):
		with patch('helper.sqlite3') as mock:
			mock.connect().commit().return_value = None
			item = helper.add_to_list('test item')
			assert item['item'] == 'test item'
			assert item['status'] == helper.NOTSTARTED

	# test the system returning all existing items in the todo list
	def test_get_all_items(self):
		test_data = ['first item','second item', 3]
		with patch('helper.get_all_items') as mock:
			mock.return_value = test_data
			items = helper.get_all_items()
			assert items == test_data

	# same as the previous test, but this time with an empty list
	def test_get_all_items1(self):
		test_data = []
		with patch('helper.get_all_items') as mock:
			mock.return_value = test_data
			items = helper.get_all_items()
			assert items == test_data

	# test getting items from a specific range of indices, test for multiple indices
	@patch('helper.get_all_items')	
	def test_get_item_range(self, fake_items):
		fake_items.return_value = []
		for i in range(-300, 100):
			fake_items.append([f'item {i}',helper.INPROGRESS])
		
		test_data = [[1,3],[4,13],[32,0],[0,0],[-200,-32]]
		real_items = helper.get_all_items()

		for td in test_data:
			assert helper.get_item_range(td[1],td[0]) == real_items[td[0]:td[1]]

	# test that the item status is updated accordingly
	def test_started(self):
		with patch('helper.sqlite3') as mock:
			result = helper.update_status('test item',helper.INPROGRESS)
			assert result == {'test item':'In Progress'}

# test getting a random task from the list of tasks
@patch('helper.get_all_items')
def test_get_random_task(fake_method):
	fake_method.return_value = ['Some task']
	task = helper.get_random_task()
	assert task == 'No tasks left'

class TestHelper2:
	# test receiving an item
	@patch('builtins.print')
	def test_Getitem(self, fake_print):
		item = helper.get_item('test item')
		assert item == helper.INPROGRESS
		fake_print.assert_called_with('test item')

	# test deleting an item
	@patch('helper.sqlite3')	
	def test_del(self, fakedb):
		aa = helper.delete_item('test item')
		assert aa == {'item':'test item'}


# test the complete functionality of the helper class
@patch('helper.sqlite3')
def test_all(fakedb):
	items = ['first','second','last']

	for item in items:
		tmp = helper.add_to_list(item)
		# Hardcoded constant, also inconsistency
		check.equal(tmp, {'item':item, 'status':'Not Started'})

	tmp = helper.update_status('first',helper.COMPLETED)
	assert tmp == {'first':helper.COMPLETED}

	tmp = helper.get_all_items()
	assert tmp['count'] == len(items)

	
