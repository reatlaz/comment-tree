import './App.css';

import React, { useEffect, useState } from 'react';


const Comment = ({ comments }) => {
  const [isError, setIsError] = useState(false);
  const deleteComment = (id) => {
    fetch('/comments/' + id + '/', {
      method: 'POST'
    })
      .then(resp => resp.json())
      .then(data => {
        console.log('deleted: ', data);
        window.location.reload(false);
      })
      .catch(err => {
        setIsError(true)
      })
  }
  return (
    <div className='comments_container'>
      {isError ? <div>Ошибка подключения</div> :
      comments.map((comment) => {
        return (
          <div key={comment.id}>
            <div className='comments_item'>

              <div className='comment-text'>
                {comment.data.text}
              </div>

              <div className='bottom-row'>
                <div className='created'>
                  {getTimeFromISOString(comment.data.created)}
                </div>
                <div
                  className='delete-comment'
                  onClick={() => deleteComment(comment.id)}
                >
                  Удалить
                </div>
              </div>

            </div>
            <div>
              {comment.children && <Comment comments={comment.children} />}
            </div>
          </div>
        );
      })}
    </div>
  );
};


function App() {
  const [comments, setComments] = useState(JSON.parse('{"data":[{"data":{"text":"Приветdfgdgfgdsf gdfsg dsfggdfgds dsagfsdafsadfsda dsaf sadf asdf sad fdsfggdfsgdfsgdsfgdfggd dgd!"},"children":[{"data":{"text":"Идет","created":"2023-03-13 04:17:39.276496+03"},"children":[{"data":{"text":"Привет!"},"children":[{"data":{"text":"Идет","created":"2023-03-13 04:17:39.276496+03"},"children":[]},{"data":{"text":"загрузка"},"children":[{"data":{"text":"(возможно)"},"children":[{"data":{"text":"загрузка"},"children":[{"data":{"text":"(возможно)"},"children":[]}]}]}]}]}]},{"data":{"text":"загрузка"},"children":[{"data":{"text":"(возможно)"},"children":[]}]}]},{"data":{"text":"Это тестовый JSON на фронте"},"children":[]}]}').data);

  const [isError, setIsError] = useState(false);

  useEffect(() => {
    fetch('/comments/', {
      mode: 'cors',
    })
      .then(resp => resp.json())
      .then(parsed => {
        setComments(parsed.data)
      })
      .catch(err => {
        setIsError(true)
      })
  }, []);

  return (
    <div className="App">
        {isError ? <div>Ошибка сервера</div>:
        <div className="comments">
          <Comment comments={comments}/>
        </div>
        }
    </div>
  );
}

function getTimeFromISOString (timestamp) {
  // return new Date(timestamp).toLocaleTimeString('ru',
  //   { timeStyle: 'short', hour12: false, timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone });
  return new Date(timestamp).toLocaleString('ru',
  { timeStyle: 'short', hour12: false, timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone, dateStyle: 'short'});
}


export default App;
