<?php
/**
* Class for making time periods readable.
*
* @author       Aidan Lister <aidan@php.net>
* @version      1.2
*/
class Duration
{
    /**
     * All in one method
     *
     * @package      Duration
     * @param        int|array  $duration   Array of time segments,
     *               or a number of seconds
     * @return       string
     */
    function toString ($duration, $periods = null)
    {
        if (!is_array($duration)) {
            $duration = Duration::int2array($duration, $periods);
        }

        return Duration::array2string($duration);
    }


    /**
     * Return an array of date segments.
     *
     * @package      Duration
     * @param        int $seconds Number of seconds to be parsed
     * @return       mixed An array containing named segments
     */
    function int2array ($seconds, $periods = null)
    {
        // Force the seconds to be numeric
        $seconds = (int)$seconds;
        
        // Define our periods
        if (!is_array($periods)) {
            $periods = array (
                    'years'     => 31556926,
                    'weeks'     => 604800,
                    'days'      => 86400,
                    'hours'     => 3600,
                    'minutes'   => 60,
                    'seconds'   => 1
                    );
        }

        // Loop through
        foreach ($periods as $period => $value)
        {
            $count = floor($seconds / $value);

            if ($count == 0) {
                continue;
            }

            $values[$period] = $count;
            $seconds = $seconds % $value;
        }

        // Return array
        if (empty($values)) {
            $values = null;
        }

        return $values;
    }


    /**
     * Return a string of time periods.
     *
     * @package      Duration
     * @param        mixed $duration An array of named segments
     * @return       string
     */
    function array2string ($duration)
    {
        if (!is_array($duration)) {
            return false;
        }

        // Loop through the interval array
        foreach ($duration as $key => $value)
        {
            // Chop the end of the duration key
            $segment_name = substr($key, 0, -1);
        
            // Create our segment in the format of eg. '4 day'
            $segment = $value . ' ' . $segment_name;

            // If the duration segment is anything other than 1, we need an 's'
            if ($value != 1)
                $segment .= 's';

            // Plop it into the array
            $array[] = $segment;
        }

        // Implode the array as a string, this way we get commas between each segment
        $str = implode(", ", $array);
        return $str;
    }

}

?> 