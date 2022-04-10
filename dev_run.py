"""Setup for development run
"""

import uvicorn


def main():
    """Entry point.
    """
    uvicorn.run(
        'web.app:app',
        debug=True,
        reload=True
    )


if __name__ == '__main__':
    main()
