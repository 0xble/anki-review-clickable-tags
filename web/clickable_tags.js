(() => {
  if (window.__reviewClickableTagsHandlersLoaded) {
    return;
  }
  window.__reviewClickableTagsHandlersLoaded = true;

  const MESSAGE_PREFIX = "review_clickable_tags:";
  const SINGLE_CLICK_DELAY_MS = 220;
  let clickTimer = null;

  const getBridgeCommand = () => window.bridgeCommand || window.pycmd;

  const getButton = (event) => {
    const { target } = event;
    if (!(target instanceof Element)) {
      return null;
    }
    return target.closest(".rct-tag");
  };

  const sendAction = (button, action) => {
    const tag = button.dataset.rctTag || "";
    const bridgeCommand = getBridgeCommand();
    if (!tag || typeof bridgeCommand !== "function") {
      return;
    }
    const deck = button.dataset.rctDeck || "";
    const payload = JSON.stringify({ action, tag, deck });
    bridgeCommand(MESSAGE_PREFIX + payload);
  };

  document.addEventListener("click", (event) => {
    const button = getButton(event);
    if (!button) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    if (clickTimer) {
      clearTimeout(clickTimer);
    }
    clickTimer = window.setTimeout(() => {
      sendAction(button, "click");
      clickTimer = null;
    }, SINGLE_CLICK_DELAY_MS);
  });

  document.addEventListener("dblclick", (event) => {
    const button = getButton(event);
    if (!button) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    if (clickTimer) {
      clearTimeout(clickTimer);
      clickTimer = null;
    }
    sendAction(button, "dblclick");
  });
})();
