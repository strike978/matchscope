<div align="center">
  <img src="icon.png" alt="MatchScope Logo" width="64" height="64">
</div>

## [0.8-BETA] - 2025-07-06

### Major Changes

- **Improved Reliability:**

  - Major bug fixes and error handling improvements for match retrieval and processing
  - More robust handling of network errors and API failures

- **Community Filtering Enhancements:**

  - Optimized and stabilized community filtering logic
  - Improved UI feedback and error messages for community selection

- **Pause/Resume Improvements:**

  - Enhanced pause/resume controls for long-running operations
  - Improved thread safety and UI responsiveness during pausing/resuming

- **Progress Tracking:**

  - More accurate progress bars, time estimates, and status messages

- **UI/UX Polish:**
  - Smoother experience, clearer error messages, and minor visual improvements

---

## [0.6-BETA] - 2025-07-06

### Major Changes

- **Enhanced Beta Release:**

  - Version bump to 0.6-BETA with significant new features
  - Continued refinement and improvement while maintaining beta status
  - Enhanced functionality for advanced users

- **Community Filtering:**
  - **NEW:** Added comprehensive community filtering functionality
  - Users can now filter matches by specific genetic communities/populations
  - Automatically fetches available communities for each DNA test
  - Smart filtering skips matches that don't belong to selected communities
  - Improves targeted analysis for specific genetic groups

### UI/UX Improvements

- **Enhanced Match Options Interface:**

  - Redesigned match options with improved card-based layout
  - Better organization of filtering controls
  - Cleaner visual separation between different option groups

- **Time Estimation:**

  - **NEW:** Added estimated time remaining for both page fetching and match processing phases
  - Real-time updates based on current processing speed
  - Better user feedback during long-running operations

- **Progress Indicators:**
  - Improved progress tracking with separate phases for fetching and processing
  - More detailed status messages throughout the workflow
  - Better visual feedback for user actions

### Technical Improvements

- **API Integration:**

  - Integrated sharedmigrations endpoint for community data retrieval
  - Enhanced error handling for community filtering operations
  - Improved robustness of match processing pipeline

- **Performance Optimizations:**
  - Optimized community filtering logic
  - Better memory management during large match processing
  - Improved thread safety for UI updates

### Bug Fixes

- Fixed issues with custom centimorgan range calculations
- Improved stability during pause/resume operations
- Better error handling for network timeouts
- Fixed UI responsiveness during heavy processing

---

## [0.5-BETA] - 2025-07-05

### Major Changes

- **BETA Release:**

  - Version bump to 0.5-BETA, marking the transition from alpha to beta status.
  - Improved stability, reliability, and readiness for broader user testing.

- **Advanced Custom Filtering:**
  - Users can now specify custom centimorgan (cM) ranges and filter matches with greater flexibility, making it easier to target specific match types.

### Notable Updates

- **UI/UX Improvements:**

  - Polished interface and workflow for a smoother user experience.
  - Improved error messages and feedback throughout the app.
  - Version string and documentation updated to reflect BETA status.

- **Performance & Bug Fixes:**
  - Minor bug fixes and optimizations for better performance and reliability.

---

## [0.1.5-alpha] - 2025-07-04

### Major Changes

- **Modern UI with Flet:**  
  Migrated from a classic Tkinter interface to a modern, responsive Flet desktop app with Material Design elements.

- **Real-Time Ethnicity Visualization:**  
  Ethnicity regions for each match are now displayed as interactive horizontal bar charts, replacing plain text.

- **Progress & Status Feedback:**  
  Added a progress bar and live status labels for both match retrieval and processing, giving clear feedback throughout.  
  The app now tracks and displays progress based on the number of matches being processed, rather than focusing on pages.

- **Improved Error Handling:**  
  Errors and completion messages are shown in a snackbar for better visibility.

### Fixed & Improved

- **Match-Based Progress:**  
  Progress and status now reflect the number of matches being fetched and processed, not the number of pages, making the workflow more intuitive and user-focused.

---

**Summary:**  
This release is a complete overhaul of MatchScope, transforming it from a basic Tkinter tool into a modern, user-friendly desktop app with advanced visualization, robust progress tracking, and a much improved, match-centric workflow.
