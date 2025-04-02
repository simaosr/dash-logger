import React, { useState, useEffect, useRef } from "react";
import PropTypes from "prop-types";
// import "../../../dash_logger/assets/dash_logger.css";

/**
 * DashLogger component for displaying logs in real-time.
 */
const DashLogger = ({
  id,
  loggerName,
  loggerNames,
  maxLogs = 100,
  className = "",
  style = {},
  twoColumns = false,
  timestampFormat = "%Y-%m-%d %H:%M:%S",
}) => {
  const [logs, setLogs] = useState([]);
  const [lastTimestamp, setLastTimestamp] = useState(null);
  const logContainerRef = useRef(null);
  const eventSourcesRef = useRef([]);

  // Determine if this is a combined logger
  const isCombined = loggerNames && loggerNames.length > 0;

  // Create default style object
  const defaultStyle = {
    height: "300px",
    overflow: "auto",
    border: "1px solid #ddd",
    padding: "10px",
    fontFamily: "monospace",
    backgroundColor: "#f5f5f5",
  };

  // Merge default styles with user-provided styles
  const combinedStyle = { ...defaultStyle, ...style };

  // Format a log message as a React element
  const formatLogMessage = (log) => {
    // Create the log entry with proper CSS classes
    const levelClass = log.level ? log.level.toLowerCase() : "info";

    // Handle multiline messages
    const messageLines = log.message.split("\n").map((line, i) => (
      <React.Fragment key={i}>
        {i > 0 && <br />}
        {line}
      </React.Fragment>
    ));

    // Format the timestamp to something like '%H:%M:%S'
    const formattedTimestamp = strftime(timestampFormat, Date(log.timestamp));

    // Render the log entry depending of the twoColumns prop
    if (twoColumns) {
      return (
        <div
          className={`dash-logger-entry ${levelClass}`}
          key={`${log.timestamp}-${Math.random()}`}
        >
          <span className="dash-logger-timestamp">[{formattedTimestamp}]</span>
          <span className="dash-logger-message">{messageLines}</span>
        </div>
      );
    }

    // Default rendering
    return (
      <div
        className={`dash-logger-entry ${levelClass}`}
        key={`${log.timestamp}-${Math.random()}`}
      >
        <div className="dash-logger-metadata">
          <span className="dash-logger-timestamp">[{formattedTimestamp}]</span>
          {isCombined && (
            <span className="dash-logger-name">{log.logger_name}</span>
          )}
        </div>
        <div className="dash-logger-content">{messageLines}</div>
      </div>
    );
  };

  // Set up SSE (Server-Sent Events) connection
  const setupSSE = () => {
    // Clean up any existing event sources
    eventSourcesRef.current.forEach((es) => es.close());
    eventSourcesRef.current = [];

    const setupEventSource = (name) => {
      console.log(`Attempting to connect to logger: ${name}`);

      let eventSource = null;

      eventSource = new EventSource(`/logs/stream/${name}`);

      eventSource.onmessage = (event) => {
        try {
          const logData = JSON.parse(event.data);
          setLogs((prevLogs) => {
            // Add new log and maintain order
            const updatedLogs = [...prevLogs, logData];

            // Sort by timestamp if needed
            updatedLogs.sort((a, b) => {
              return new Date(a.timestamp) - new Date(b.timestamp);
            });

            // Limit log count
            if (updatedLogs.length > maxLogs) {
              return updatedLogs.slice(updatedLogs.length - maxLogs);
            }
            return updatedLogs;
          });
        } catch (error) {
          console.error("Error processing log message:", error);
        }
      };

      eventSource.onerror = (error) => {
        console.error(`Error in SSE connection for logger ${name}:`, error);

        // Only try to reconnect if the component is still mounted
        // and we're not in the middle of reconnecting
        const isReconnecting = eventSourcesRef.current.reconnecting;
        if (!isReconnecting) {
          eventSourcesRef.current.reconnecting = true;
          eventSource.close();

          // Try to reconnect after a delay with exponential backoff
          console.log(`Will attempt to reconnect to ${name} in 5 seconds`);
          setTimeout(() => {
            // Only reconnect if the component is still mounted
            if (eventSourcesRef.current) {
              console.log(`Reconnecting to logger: ${name}`);
              const newEventSource = setupEventSource(name);
              eventSourcesRef.current = eventSourcesRef.current.filter(
                (es) => es !== eventSource
              );
              eventSourcesRef.current.push(newEventSource);
              eventSourcesRef.current.reconnecting = false;
            }
          }, 5000);
        }
      };

      // Add onopen handler to confirm successful connection
      eventSource.onopen = () => {
        console.log(`Successfully connected to logger: ${name}`);
      };

      return eventSource;
    };

    // Set up event sources for all loggers
    if (isCombined) {
      loggerNames.forEach((name) => {
        const es = setupEventSource(name);
        eventSourcesRef.current.push(es);
      });
    } else {
      const name = loggerName || id;
      const es = setupEventSource(name);
      eventSourcesRef.current.push(es);
    }
  };

  // Scroll to bottom when logs change
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  // Set up SSE
  useEffect(() => {
    // Add a small delay before initial connection attempt
    const connectionTimer = setTimeout(() => {
      setupSSE();
    }, 1000); // 1 second delay

    // Clean up on unmount
    return () => {
      clearTimeout(connectionTimer);
      // Close all event sources
      eventSourcesRef.current.forEach((es) => es.close());
      eventSourcesRef.current = [];
    };
  }, [loggerName, isCombined, loggerNames, id]); // Add dependencies

  return (
    <div
      id={id}
      className={`dash-logger ${className || ""}`}
      style={combinedStyle}
      ref={logContainerRef}
    >
      {logs.map(formatLogMessage)}
    </div>
  );
};

DashLogger.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string.isRequired,

  /**
   * Name of the logger to display (for single logger view)
   */
  loggerName: PropTypes.string,

  /**
   * Names of loggers to display (for combined view)
   */
  loggerNames: PropTypes.arrayOf(PropTypes.string),

  /**
   * Maximum number of logs to display
   */
  maxLogs: PropTypes.number,

  /**
   * Additional class name for the logger container
   */
  className: PropTypes.string,

  /**
   * Additional inline styles for the logger container
   */
  style: PropTypes.object,

  /**
   * Whether to display logs in two columns (timestamp and message)
   */
  twoColumns: PropTypes.bool,

  /**
   * The format string for the timestamp
   */
  timestampFormat: PropTypes.string,
};

/* Port of strftime() by T. H. Doan (https://thdoan.github.io/strftime/)
 *
 * Day of year (%j) code based on Joe Orost's answer:
 * http://stackoverflow.com/questions/8619879/javascript-calculate-the-day-of-the-year-1-366
 *
 * Week number (%V) code based on Taco van den Broek's prototype:
 * http://techblog.procurios.nl/k/news/view/33796/14863/calculate-iso-8601-week-and-year-in-javascript.html
 */
function strftime(sFormat, date) {
  if (typeof sFormat !== "string") {
    return "";
  }

  if (!(date instanceof Date)) {
    date = new Date();
  }

  const nDay = date.getDay();
  const nDate = date.getDate();
  const nMonth = date.getMonth();
  const nYear = date.getFullYear();
  const nHour = date.getHours();
  const nTime = date.getTime();
  const aDays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const aMonths = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const aDayCount = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  const isLeapYear = () =>
    (nYear % 4 === 0 && nYear % 100 !== 0) || nYear % 400 === 0;
  const getThursday = () => {
    const target = new Date(date);
    target.setDate(nDate - ((nDay + 6) % 7) + 3);
    return target;
  };
  const zeroPad = (nNum, nPad) => (Math.pow(10, nPad) + nNum + "").slice(1);

  return sFormat.replace(/%[a-z]+\b/gi, (sMatch) => {
    return (
      ({
        "%a": aDays[nDay].slice(0, 3),
        "%A": aDays[nDay],
        "%b": aMonths[nMonth].slice(0, 3),
        "%B": aMonths[nMonth],
        "%c": date.toUTCString().replace(",", ""),
        "%C": Math.floor(nYear / 100),
        "%d": zeroPad(nDate, 2),
        "%e": nDate,
        "%F": new Date(nTime - date.getTimezoneOffset() * 60000)
          .toISOString()
          .slice(0, 10),
        "%G": getThursday().getFullYear(),
        "%g": (getThursday().getFullYear() + "").slice(2),
        "%H": zeroPad(nHour, 2),
        "%I": zeroPad(((nHour + 11) % 12) + 1, 2),
        "%j": zeroPad(
          aDayCount[nMonth] + nDate + (nMonth > 1 && isLeapYear() ? 1 : 0),
          3
        ),
        "%k": nHour,
        "%l": ((nHour + 11) % 12) + 1,
        "%m": zeroPad(nMonth + 1, 2),
        "%n": nMonth + 1,
        "%M": zeroPad(date.getMinutes(), 2),
        "%p": nHour < 12 ? "AM" : "PM",
        "%P": nHour < 12 ? "am" : "pm",
        "%s": Math.round(nTime / 1000),
        "%S": zeroPad(date.getSeconds(), 2),
        "%u": nDay || 7,
        "%V": (() => {
          const target = getThursday();
          const n1stThu = target.valueOf();
          target.setMonth(0, 1);
          const nJan1 = target.getDay();

          if (nJan1 !== 4) {
            target.setMonth(0, 1 + ((4 - nJan1 + 7) % 7));
          }

          return zeroPad(1 + Math.ceil((n1stThu - target) / 604800000), 2);
        })(),
        "%w": nDay,
        "%x": date.toLocaleDateString(),
        "%X": date.toLocaleTimeString(),
        "%y": (nYear + "").slice(2),
        "%Y": nYear,
        "%z": date.toTimeString().replace(/.+GMT([+-]\d+).+/, "$1"),
        "%Z": date.toTimeString().replace(/.+\((.+?)\)$/, "$1"),
        "%Zs": new Intl.DateTimeFormat("default", {
          timeZoneName: "short",
        })
          .formatToParts(date)
          .find((oPart) => oPart.type === "timeZoneName")?.value,
      }[sMatch] || "") + "" || sMatch
    );
  });
}

export default DashLogger;
