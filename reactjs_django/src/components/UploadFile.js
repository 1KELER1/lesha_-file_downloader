import React, {useState, useEffect} from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

function UploadFile() {
    const [filename, setFilename] = useState('')
    const [files, setFiles] = useState([{}])
    const [status, setstatus] = useState('')
    const [user, setUser] = useState(null)
    const navigate = useNavigate()

    let api = 'http://127.0.0.1:8000/api'

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            navigate('/login');
            return;
        }
        
        // Устанавливаем токен в заголовок по умолчанию
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Получаем информацию о пользователе
        axios.get(`${api.replace('/api', '')}/api/user/`).then(
            response => {
                setUser(response.data);
                // После получения информации о пользователе загружаем файлы
                getFiles();
            }
        ).catch(error => {
            console.error('Ошибка при получении данных пользователя:', error);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            navigate('/login');
        });
    }, [navigate]);

    const saveFile = () => {
        console.log('Button clicked')

        let formData = new FormData();
        formData.append("pdf", filename)

        let axiosConfig = {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        }

        console.log(formData)
        axios.post(api + '/files/', formData, axiosConfig).then(
            response => {
                console.log(response)
                setstatus('Файл успешно загружен')
                getFiles() // Обновляем список файлов после загрузки
            }
        ).catch(error => {
            console.log(error)
            if (error.response && error.response.status === 401) {
                // Если ошибка авторизации, перенаправляем на страницу входа
                navigate('/login');
            }
        })
    }

    const getFiles = () => {
        axios.get(api + '/files/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        }).then(
            response => {
                setFiles(response.data)
            }
        ).catch(error => {
            console.log(error)
            if (error.response && error.response.status === 401) {
                navigate('/login');
            }
        })
    }

    const forceDownload = (response, title, originalFileName) => {
        console.log(response)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        
        // Извлекаем оригинальное имя файла и расширение
        let fileExtension = '.pdf'; // По умолчанию
        if (originalFileName) {
            const lastDotPosition = originalFileName.lastIndexOf('.');
            if (lastDotPosition !== -1) {
                fileExtension = originalFileName.substring(lastDotPosition);
            }
        }
        
        link.setAttribute('download', title + fileExtension)
        document.body.appendChild(link)
        link.click()
    }

    const downloadWithAxios = (url, title) => {
        // Получаем оригинальное имя файла из URL
        const originalFileName = url.split('/').pop();

        axios({
            method: 'get',
            url,
            responseType: 'arraybuffer',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        }).then((response) => {
            forceDownload(response, title, originalFileName)
        }).catch((error) => {
            console.log(error)
            if (error.response && error.response.status === 401) {
                navigate('/login');
            }
        })
    }

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete axios.defaults.headers.common['Authorization'];
        navigate('/login');
    };

    const goToProfile = () => {
        navigate('/profile');
    };

    return (
        <div className="container-fluid">
            <div className="d-flex justify-content-between align-items-center mt-2 mb-3">
                <h2 className="text-center alert alert-danger">Загрузка и скачивание файлов - Django 4 и React JS 18</h2>
                <div>
                    {user && (
                        <div className="d-flex">
                            <button onClick={goToProfile} className="btn btn-info me-2">
                                {user.username}
                            </button>
                            <button onClick={handleLogout} className="btn btn-danger">
                                Выйти
                            </button>
                        </div>
                    )}
                </div>
            </div>

            <div className="row">
                <div className="col-md-4">
                    <h2 className="alert alert-success">Раздел загрузки файлов</h2>

                    <form>
                        <div className="form-group">
                            <label htmlFor="exampleFormControlFile1" className="float-left">Выберите любой файл для загрузки</label>
                            <input type="file" onChange={e => setFilename(e.target.files[0])} className="form-control" />
                            <small className="form-text text-muted">Поддерживаются файлы любых форматов</small>
                        </div>

                        <button type="button" onClick={saveFile} className="btn btn-primary float-left mt-2">Отправить</button>
                        <br />
                        <br />
                        <br />

                        {status ? <h2>{status}</h2> : null}
                    </form>
                </div>

                <div className="col-md-7">
                    <h2 className="alert alert-success">Список загруженных файлов</h2>

                    <table className="table table-bordered mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Название файла</th>
                                <th scope="col">Скачать</th>
                            </tr>
                        </thead>
                        <tbody>
                            {files.map(file => {
                                const fileName = file.pdf ? file.pdf.split('/').pop() : '';
                                return (
                                    <tr>
                                        <td>{fileName}</td>
                                        <td><a href="" target="_blank"></a>
                                            <button onClick={() => downloadWithAxios(file.pdf, file.id)} className="btn btn-success">Скачать</button>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}

export default UploadFile
