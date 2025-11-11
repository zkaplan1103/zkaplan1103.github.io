function toggleExpansion(element) {
    const card = element.closest('.project-card');
    const collapseNote = card.querySelector('.collapse-note');

    if (card.classList.contains('expanded')) {
        // Collapse the card
        card.classList.remove('expanded');
        collapseNote.style.display = 'none';
        card.style.maxHeight = '280px';
    } else {
        // First, add the expanded class to remove text clamping
        card.classList.add('expanded');
        collapseNote.style.display = 'block';

        // Use requestAnimationFrame to ensure DOM has updated
        requestAnimationFrame(() => {
            // Get the actual height needed after DOM update
            const actualHeight = card.scrollHeight;

            // Set to actual height for smooth expansion
            card.style.maxHeight = actualHeight + 'px';
        });

        // Add click event to collapse note
        collapseNote.onclick = function() {
            toggleExpansion(element);
        };
    }
}

// Handle Space Race hover popup
document.addEventListener('DOMContentLoaded', function() {
    const spaceRaceCard = document.querySelector('.project-card-with-hover');
    const popup = document.querySelector('.hover-image-popup');

    if (spaceRaceCard && popup) {
        spaceRaceCard.addEventListener('mouseenter', function() {
            popup.style.opacity = '1';
            popup.style.pointerEvents = 'auto';
        });

        spaceRaceCard.addEventListener('mouseleave', function() {
            popup.style.opacity = '0';
            popup.style.pointerEvents = 'none';
        });
    }

    // Create interactive grid background only on non-mobile devices
    if (window.innerWidth > 768) {
        createInteractiveGrid();
    }
});

function createInteractiveGrid() {
    const gridContainer = document.getElementById('grid-background');
    const cellSize = 80; // Size of each grid cell in pixels
    let gridCells = [];

    // Wait for page to load completely then get full height
    setTimeout(() => {
        const main = document.querySelector('main');
        const fullHeight = main.scrollHeight;
        const fullWidth = window.innerWidth;

        console.log(`Main element height: ${fullHeight}px, width: ${fullWidth}px`);

        const cols = Math.ceil(fullWidth / cellSize);
        const rows = Math.ceil(fullHeight / cellSize);

        console.log(`Creating grid: ${cols} cols x ${rows} rows`);

        // Create grid cells and store references
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                cell.style.width = cellSize + 'px';
                cell.style.height = cellSize + 'px';
                cell.style.left = (col * cellSize) + 'px';
                cell.style.top = (row * cellSize) + 'px';
                cell.dataset.row = row;
                cell.dataset.col = col;

                gridContainer.appendChild(cell);
                gridCells.push(cell);
            }
        }

        // Track mouse position and activate cells
        document.addEventListener('mousemove', function(e) {
            // Calculate which grid cell the mouse is over
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const mouseY = e.clientY + scrollTop;
            const mouseX = e.clientX;

            const col = Math.floor(mouseX / cellSize);
            const row = Math.floor(mouseY / cellSize);

            // Find and activate the corresponding cell
            const cell = gridCells.find(c =>
                parseInt(c.dataset.row) === row && parseInt(c.dataset.col) === col
            );

            if (cell && !cell.classList.contains('active')) {
                cell.classList.add('active');

                // Store timeout ID on the element
                if (cell.fadeTimeout) {
                    clearTimeout(cell.fadeTimeout);
                }

                cell.fadeTimeout = setTimeout(() => {
                    cell.classList.remove('active');
                }, 2000);
            }
        });

        console.log('Grid created successfully');
    }, 200);

    // Regenerate grid on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            gridContainer.innerHTML = '';
            createInteractiveGrid();
        }, 250);
    });
}