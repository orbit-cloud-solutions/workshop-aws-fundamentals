import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

const apiUrl = 'https://vsteh4ih09.execute-api.eu-central-1.amazonaws.com/v1'; // update with your URL API

function CrudApp() {
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState({
    ProductID: '',
    ProductName: '',
    Price: '',
    CreatedAt: '',
    UpdatedAt: ''
  });
  const [loading, setLoading] = useState(false);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const response = await axios.get(apiUrl);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchItem = async (ProductID) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/${ProductID}`);
      setCurrentItem(response.data);
    } catch (error) {
      console.error('Error fetching item:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveItem = async () => {
    setLoading(true);
    const currentDate = new Date().toISOString();

    const itemToSave = {
      ...currentItem,
      UpdatedAt: currentDate,
      CreatedAt: currentItem.ProductID ? currentItem.CreatedAt : currentDate
    };

    if (!itemToSave.ProductID) {
      itemToSave.ProductID = uuidv4();
    }

    try {
      if (itemToSave.ProductID) {
        await axios.put(`${apiUrl}/${itemToSave.ProductID}`, itemToSave);
        alert('Item updated successfully');
      } else {
        await axios.post(apiUrl, itemToSave);
        alert('Item created successfully');
      }
      setCurrentItem({
        ProductID: '',
        ProductName: '',
        Price: '',
        CreatedAt: '',
        UpdatedAt: ''
      });
      fetchItems();
    } catch (error) {
      console.error('Error saving item:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (ProductID) => {
    setLoading(true);
    try {
      await axios.delete(`${apiUrl}/${ProductID}`);
      alert('Item deleted successfully');
      fetchItems();
    } catch (error) {
      console.error('Error deleting item:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <div className="crud-container">
      <h1>Workshop CRUD App</h1>
      {loading && <p>Loading...</p>}

      {/* Seznam položek */}
      <div className="items-list">
        <h2>Items</h2>
        <ul>
          {items.map(item => (
            <li key={item.ProductID}>
              {item.ProductName} - ${item.Price}
              <div className="button-container">
                <button onClick={() => fetchItem(item.ProductID)}>Edit</button>
                <button onClick={() => deleteItem(item.ProductID)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Formulář pro přidání/aktualizaci položky */}
      <div className="item-form">
        <h2>{currentItem.ProductID ? 'Edit Product' : 'Add Product'}</h2>
        <input
          type="text"
          placeholder="Product Name"
          value={currentItem.ProductName}
          onChange={(e) => setCurrentItem({ ...currentItem, ProductName: e.target.value })}
        />
        <input
          type="number"
          placeholder="Price"
          value={currentItem.Price}
          onChange={(e) => setCurrentItem({ ...currentItem, Price: e.target.value })}
        />
        <button onClick={saveItem}>
          {currentItem.ProductID ? 'Update' : 'Create'}
        </button>
      </div>
    </div>
  );
}

export default CrudApp;
