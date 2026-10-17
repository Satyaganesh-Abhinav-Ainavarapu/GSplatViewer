import style from './Submit_button.module.css';

export default function Submit_button({ onClick }) {
  return (
    <button className={style.submit} onClick={onClick}>
      Submit Button
    </button>
  );
}