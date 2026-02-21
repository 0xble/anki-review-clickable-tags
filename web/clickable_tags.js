(() => {
  if (window.__reviewClickableTagsLoaded) {
    return;
  }
  window.__reviewClickableTagsLoaded = true;

  const MESSAGE_PREFIX = "review_clickable_tags:";
  const SINGLE_CLICK_DELAY_MS = 220;
  let clickTimer = null;

  const sendAction = (button, action) => {
    const tag = button.dataset.rctTag || "";
    if (!tag) {
      return;
    }
    const deck = button.dataset.rctDeck || "";
    const payload = JSON.stringify({ action, tag, deck });
    pycmd(MESSAGE_PREFIX + payload);
  };

  document.addEventListener("click", (event) => {
    const button = event.target.closest(".rct-tag");
    if (!button) {
      return;
    }
    event.preventDefault();
    if (clickTimer) {
      clearTimeout(clickTimer);
    }
    clickTimer = window.setTimeout(() => {
      sendAction(button, "click");
      clickTimer = null;
    }, SINGLE_CLICK_DELAY_MS);
  });

  document.addEventListener("dblclick", (event) => {
    const button = event.target.closest(".rct-tag");
    if (!button) {
      return;
    }
    event.preventDefault();
    if (clickTimer) {
      clearTimeout(clickTimer);
      clickTimer = null;
    }
    sendAction(button, "dblclick");
  });
})();
