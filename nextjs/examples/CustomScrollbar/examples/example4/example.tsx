const RoCtor = (window as any).ResizeObserver as typeof ResizeObserver | undefined;
const ro = RoCtor ? new RoCtor(() => updateThumb()) : null;


// ================================

const RoCtor = (window as any).ResizeObserver;
const ro = RoCtor ? new RoCtor(() => updateThumb()) : null;


// ==============================

const ro = (window as any).ResizeObserver
  ? new (window as any).ResizeObserver(() => updateThumb())
  : null;
