import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchArticle } from '../utils/api';
import ArticleCard from '../components/ArticleCard';

const Article = () => {
    const { id } = useParams();
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getArticle = async () => {
            try {
                const data = await fetchArticle(id);
                setArticle(data);
            } catch (error) {
                console.error('Error fetching article:', error);
            } finally {
                setLoading(false);
            }
        };

        getArticle();
    }, [id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!article) {
        return <div>Article not found.</div>;
    }

    return (
        <div className="article-page">
            <h1>{article.title}</h1>
            <img src={article.image} alt={article.title} />
            <p>{article.content}</p>
            <h2>Related Products</h2>
            <div className="related-products">
                {article.relatedProducts.map(product => (
                    <ArticleCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export default Article;