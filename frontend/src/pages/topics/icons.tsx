interface IconProps {
  size?: number;
  className?: string;
  isActive?: boolean; // We add this to handle the "Selected" state
}

export const BrazilIcon: React.FC<IconProps> = ({
  size = 24,
  className = "",
  isActive = false,
}) => {
  // If active, we use white. If not, we use the Brazil palette.
  const green = isActive ? "currentColor" : "#009739";
  const yellow = isActive ? "currentColor" : "#FEDD00";
  const blue = isActive ? "#050636" : "#012169";

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Outer Flag (Green) */}
      <rect
        x="2"
        y="4"
        width="20"
        height="16"
        rx="2"
        fill={green}
        fillOpacity={isActive ? "0.2" : "1"}
        stroke={isActive ? "currentColor" : "none"}
        strokeWidth="2"
      />

      {/* Diamond (Yellow) */}
      <path d="M12 7l7 5-7 5-7-5 7-5z" fill={yellow} />

      {/* Circle (Blue) */}
      <circle cx="12" cy="12" r="2.5" fill={blue} />
    </svg>
  );
};

export const IconA: React.FC<IconProps> = ({
  size = 24,
  className = "",
  isActive = false,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M5 19L12 5l7 14" />
    <path d="M7 14h10" />
  </svg>
);

export const IconB: React.FC<IconProps> = ({
  size = 24,
  className = "",
  isActive = false,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M7 5h4.5a3.5 3.5 0 0 1 0 7H7" />
    <path d="M7 12h5.5a3.5 3.5 0 0 1 0 7H7V5z" />
  </svg>
);

interface IconProps {
  size?: number;
  className?: string;
}
