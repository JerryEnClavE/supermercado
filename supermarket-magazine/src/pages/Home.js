import React, { useEffect, useState } from 'react';
import ArticleCard from '../components/ArticleCard';
import { fetchArticles } from '../utils/api';

const Home = () => {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        const getArticles = async () => {
            const data = await fetchArticles();
            setArticles(data);
        };

        getArticles();
    }, []);

    return (
        <div className="home">
            <h1>Welcome to the Supermarket Magazine</h1>
            <h2>Featured Articles</h2>
            <div className="article-list">
                {articles.map(article => (
                    <ArticleCard key={article.id} article={article} />
                ))}
            </div>
        </div>
    );
};

export default Home;