import logo from './logo.svg';
import './App.css';

import React, { useEffect, useState } from 'react';


const deleteComment = (id) => {
  fetch('/comments/' + id + '/', {
    method: 'POST'
  })
    .then(resp => resp.json())
    .then(data => {
      console.log('deletion response: ', data)
      window.location.reload(false)
    })
    .catch(err => {
      console.log(err)
    })
}

const Comment = ({ data }) => {
  return (
    <div className='comments_container'>
      {data.map((parent, index) => {
        return (
          <div key={parent.created}>
            <div className='comments_item'>
              <div>
                {parent.text}
              </div>
              <div className='right-row'>
                <div className='created'>
                  {getTimeFromISOString(parent.created)}
                </div>
                <div
                  className='delete-comment'
                  onClick={() => deleteComment(parent.id)}
                >
                  Удалить
                </div>
              </div>

            </div>
            <div>
              {parent.replies && <Comment data={parent.replies} />}
            </div>
          </div>
        );
      })}
    </div>
  );
};


function App() {
  const [comments, setComments] = useState(JSON.parse('{"data":[{"text":"Привет!","replies":[{"text":"Идет","replies":[],"created": "2023-03-13 04:17:39.276496+03"},{"text":"загрузка","replies":[{"text":"(возможно)","replies":[]}]}]},{"text":"Это тестовый JSON на фронте","replies":[]}]}').data);

  useEffect(() => {
    fetch('/comments/', {
      mode: 'cors',
    })
      .then(resp => resp.json())
      .then(parsed => {
        setComments(parsed.data)
      })
      .catch(err => {
        console.log(err)
      })
  }, []);

  return (
    <div className="App">
      <div className="comments">
        <Comment data={comments}/>
      </div>
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
