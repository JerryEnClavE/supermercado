import React, { useState, useEffect } from 'react';
import { updateProduct, getProductById } from '../utils/api';

const ProductEditor = ({ productId }) => {
    const [product, setProduct] = useState({ name: '', price: '', description: '' });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const data = await getProductById(productId);
                setProduct(data);
                setLoading(false);
            } catch (err) {
                setError('Error fetching product data');
                setLoading(false);
            }
        };

        fetchProduct();
    }, [productId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProduct({ ...product, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updateProduct(productId, product);
            alert('Product updated successfully!');
        } catch (err) {
            setError('Error updating product');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>
                    Product Name:
                    <input type="text" name="name" value={product.name} onChange={handleChange} required />
                </label>
            </div>
            <div>
                <label>
                    Price:
                    <input type="number" name="price" value={product.price} onChange={handleChange} required />
                </label>
            </div>
            <div>
                <label>
                    Description:
                    <textarea name="description" value={product.description} onChange={handleChange} required />
                </label>
            </div>
            <button type="submit">Update Product</button>
        </form>
    );
};

export default ProductEditor;