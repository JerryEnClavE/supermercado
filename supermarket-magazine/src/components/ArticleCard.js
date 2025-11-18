import React from 'react';

const ArticleCard = ({ article }) => {
    return (
        <div className="article-card">
            <img src={article.image} alt={article.title} className="article-image" />
            <h2 className="article-title">{article.title}</h2>
            <p className="article-summary">{article.summary}</p>
            <a href={`/articles/${article.id}`} className="read-more">Read More</a>
        </div>
    );
};

export default ArticleCard;