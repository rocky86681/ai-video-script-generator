export default function Footer() {
  return (
    <footer className="app-footer">
      <p className="footer-text">
        Built with ❤️ using <a href="https://fastapi.tiangolo.com" target="_blank" rel="noopener">FastAPI</a>,{' '}
        <a href="https://react.dev" target="_blank" rel="noopener">React</a>, and{' '}
        <a href="https://openai.com" target="_blank" rel="noopener">OpenAI GPT</a>
        &nbsp;·&nbsp; AI Video Script Generator © {new Date().getFullYear()}
      </p>
    </footer>
  );
}
