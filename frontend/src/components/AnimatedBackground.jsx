export const AnimatedBackground = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      {/* Gradient Mesh Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-secondary-50 to-accent-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950" />

      {/* Floating Orbs */}
      <div className="absolute top-0 left-0 w-full h-full">
        {/* Orb 1 - Purple */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-primary-400/30 to-secondary-400/30 rounded-full blur-3xl animate-float" />

        {/* Orb 2 - Pink */}
        <div className="absolute top-1/2 right-1/4 w-80 h-80 bg-gradient-to-br from-secondary-400/25 to-accent-400/25 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s', animationDuration: '4s' }} />

        {/* Orb 3 - Orange */}
        <div className="absolute bottom-1/4 left-1/3 w-72 h-72 bg-gradient-to-br from-accent-400/20 to-primary-400/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '4s', animationDuration: '5s' }} />

        {/* Orb 4 - Blue */}
        <div className="absolute top-1/3 right-1/3 w-64 h-64 bg-gradient-to-br from-blue-400/15 to-cyan-400/15 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s', animationDuration: '6s' }} />

        {/* Orb 5 - Green */}
        <div className="absolute bottom-1/3 right-1/4 w-56 h-56 bg-gradient-to-br from-green-400/15 to-emerald-400/15 rounded-full blur-3xl animate-float" style={{ animationDelay: '3s', animationDuration: '5.5s' }} />
      </div>

      {/* Gradient Overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-t from-white/50 via-transparent to-white/30 dark:from-gray-900/50 dark:via-transparent dark:to-gray-900/30" />

      {/* Subtle grid pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:64px_64px]" />
    </div>
  );
};
